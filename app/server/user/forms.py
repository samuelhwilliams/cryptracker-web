# app/server/user/forms.py


from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, DecimalField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

from ..models import CurrencyCategory, Currency, Account


class LoginForm(FlaskForm):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )


class NewAccountForm(FlaskForm):
    currency_code = QuerySelectField('Currency Code', validators=[DataRequired()],
                                     query_factory=lambda: Currency.query.filter(~Currency.accounts.any(Account.user_id == current_user.id)).all(),
                                     get_label='code')


class NewCurrencyForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], choices=[(x, x.name) for x in CurrencyCategory])
    code = StringField('Currency Code', validators=[DataRequired()])
    name = StringField('Currency Name', validators=[DataRequired()])


class NewTransactionForm(FlaskForm):
    datetime = DateTimeField('Date & Time', validators=[Optional()])
    value = DecimalField('Value', validators=[Optional()])

    from_currency = QuerySelectField('Currency (from)', validators=[DataRequired()],
                                     query_factory=lambda: Account.query.filter_by(user_id=current_user.id).join(Account.currency).distinct(Currency.id).all(),
                                     get_label='currency.code'
                                     )
    from_volume = DecimalField('Volume (from)', validators=[DataRequired()])
    from_wallet = StringField('Wallet (from)', validators=[Optional()])

    to_currency = QuerySelectField('Currency (to)', validators=[DataRequired()],
                                     query_factory=lambda: Account.query.filter_by(user_id=current_user.id).join(Account.currency).distinct(Currency.id).all(),
                                     get_label='currency.code'
                                     )
    to_volume = DecimalField('Volume (to)', validators=[DataRequired()])
    to_wallet = StringField('Wallet (to)', validators=[Optional()])

    stake = DecimalField('Stake', validators=[Optional()])

    broker = StringField('Broker', validators=[Optional()])
    tx_id = StringField('TX ID', validators=[Optional()])
    notes = StringField('Notes', validators=[Optional()])
