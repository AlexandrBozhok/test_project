from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, NumberRange


class PayForm(FlaskForm):
    amount = IntegerField('Сума', validators=[DataRequired(), NumberRange(min=1, max=10000)])
    currency = SelectField('Валюта', choices=[('eur', 'EUR'), ('usd', 'USD'), ('rub', 'RUB')])
    description = TextAreaField('Опис')
    submit = SubmitField('Сплатити')
