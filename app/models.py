import hashlib
import uuid
from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from flask import current_app


db = SQLAlchemy()


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(128), nullable=False, unique=True)
    currency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100))


class SignHashGenerator:
    def __init__(self, required_fields: list):
        self.required_fields = required_fields

    def generate(self, params: dict):
        required_params = self.__get_required_params(params)
        original_string = ':'.join(str(item) for item in required_params.values()) + current_app.config.get('API_SECRET_KEY')
        print(original_string)
        return hashlib.sha256(original_string.encode('utf-8')).hexdigest()

    def __get_required_params(self, params: dict):
        result = {key: value for key, value in params.items() if key in self.required_fields}
        return self.__sort_params(result)

    @staticmethod
    def __sort_params(params: dict):
        return dict(sorted(params.items(), key=lambda x: x[0]))


class ParamsBuilder(ABC):
    @abstractmethod
    def create(self, params: dict, sign_generator: SignHashGenerator) -> dict:
        pass


class EURParamsBuilder(ParamsBuilder):
    def __init__(self, api_url, shop_id, currency_id):
        self.api_url = api_url
        self.shop_id = shop_id
        self.currency_id = currency_id

    def create(self, params: dict, sign_generator: SignHashGenerator) -> dict:
        params = {
            'url': self.api_url,
            'data': {
                'shop_id': self.shop_id,
                'shop_order_id': str(uuid.uuid4()),
                'amount': params.get('amount'),
                'currency': self.currency_id,
                'description': params.get('description')
            }
        }
        params['data']['sign'] = sign_generator.generate(params['data'])
        return params


class USDParamsBuilder(ParamsBuilder):
    def __init__(self, api_url, shop_id, currency_id):
        self.api_url = api_url
        self.shop_id = shop_id
        self.currency_id = currency_id

    def create(self, params: dict, sign_generator: SignHashGenerator) -> dict:
        params = {
            'url': self.api_url,
            'data': {
                'shop_id': self.shop_id,
                'shop_order_id': str(uuid.uuid4()),
                'shop_amount': params.get('amount'),
                'shop_currency': self.currency_id,
                'payer_currency': self.currency_id,
                'description': params.get('description')
            }
        }
        params['data']['sign'] = sign_generator.generate(params['data'])
        return params


class RUBParamsBuilder(ParamsBuilder):
    def __init__(self, api_url, shop_id, currency_id):
        self.api_url = api_url
        self.shop_id = shop_id
        self.currency_id = currency_id

    def create(self, params: dict, sign_generator: SignHashGenerator) -> dict:
        params = {
            'url': self.api_url,
            'data': {
                'shop_id': self.shop_id,
                'shop_order_id': str(uuid.uuid4()),
                'amount': params.get('amount'),
                'currency': self.currency_id,
                'payway': 'perfectmoney_usd',
                'description': params.get('description')
            }
        }
        params['data']['sign'] = sign_generator.generate(params['data'])
        return params
