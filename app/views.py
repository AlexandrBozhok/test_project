import requests
from flask import render_template, request, jsonify, current_app

from app import app, Currency
from app.models import SignHashGenerator, EURParamsBuilder, USDParamsBuilder, RUBParamsBuilder, Invoice, db
from app.forms import PayForm
from utils import get_current_datetime

sign_generator = SignHashGenerator(required_fields=['shop_amount', 'shop_currency', 'shop_id', 'shop_order_id',
                                                    'payer_currency', 'payway', 'currency', 'amount'])


eur_params_builder = EURParamsBuilder(api_url='https://pay.piastrix.com/en/pay',
                                      shop_id=5, currency_id=Currency.EUR.value)

usd_params_builder = USDParamsBuilder(api_url='https://core.piastrix.com/bill/create',
                                      shop_id=5, currency_id=Currency.USD.value)

rub_params_builder = RUBParamsBuilder(api_url='https://core.piastrix.com/invoice/create',
                                      shop_id=5, currency_id=Currency.RUB.value)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        form = PayForm()
        return render_template('home.html', form=form)
    else:
        form = PayForm()
        if form.validate_on_submit():
            data = request.form.to_dict()
            currency = data.get('currency')
            if currency == 'eur':
                params = eur_params_builder.create(data, sign_generator)
                current_app.logger.debug(f'EUR, params - {params}')
                save_invoice_to_db(params['data'])
                return jsonify(params)
            elif currency == 'usd':
                params = usd_params_builder.create(data, sign_generator)
                current_app.logger.debug(f'USD, params - {params}')
                save_invoice_to_db(params['data'])
                response = get_api_response(usd_params_builder.api_url, params)
                if response:
                    return response.get('data').get('url')
            elif currency == 'rub':
                params = rub_params_builder.create(data, sign_generator)
                current_app.logger.debug(f'RUB, params - {params}')
                save_invoice_to_db(params['data'])
                response = get_api_response(rub_params_builder.api_url, params)
                if response:
                    return response.get('data')
        return {}


@app.route('/statistics', methods=['GET'])
def statistics():
    invoices = Invoice.query.all()
    return render_template('invoice_stat.html', invoices=invoices)


def get_api_response(url, params):
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.post(url=url, json=params['data'], headers=headers)
    if res.status_code == 200:
        return res.json()
    return {}


def save_invoice_to_db(params):
    try:
        invoice = Invoice(
            order_id=params.get('shop_order_id'),
            currency=Currency(int(params.get('currency'))).name,
            amount=params.get('amount'),
            time=get_current_datetime(),
            description=params.get('description')
        )
        db.session.add(invoice)
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(e)
    return False
