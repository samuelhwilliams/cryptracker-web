# app/server/models.py


import enum
import datetime
from sqlalchemy import UniqueConstraint

from app.server import app, db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class CurrencyCategory(enum.Enum):
    Fiat = 1
    Crypto = 2


class Currency(db.Model):

    __tablename__ = "currencies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.Enum(CurrencyCategory), nullable=False, index=True)
    code = db.Column(db.String(5), nullable=False, index=True)
    name = db.Column(db.String(256), nullable=False)

    def __init__(self, category, code, name):
        self.category = category
        self.code = code
        self.name = name


class Account(db.Model):

    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False, index=True)
    primary_account = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    currency = db.relationship('Currency', lazy='joined', uselist=False)

    def __init__(self, user_id, currency_id, primary_account=False):
        self.user_id = user_id
        self.currency_id = currency_id
        self.primary_account = primary_account
        self.created_on = datetime.datetime.utcnow()


class Transaction(db.Model):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    value = db.Column(db.Float, nullable=False)

    from_currency = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False, index=True)
    from_volume = db.Column(db.Float, nullable=False)
    from_wallet = db.Column(db.String(256), nullable=False, default='')

    to_currency = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False, index=True)
    to_volume = db.Column(db.Float, nullable=False)
    to_wallet = db.Column(db.String(256), nullable=False, default='')

    stake = db.Column(db.Float, nullable=False)

    broker = db.Column(db.String(256), nullable=False, default='')
    tx_id = db.Column(db.String(256), nullable=False, default='')
    notes = db.Column(db.String(256), nullable=False, default='')

    def __init__(self, user_id, value, from_currency, from_volume, to_currency, to_volume,
                 stake=0, from_wallet='', to_wallet='', broker='', tx_id='', notes='', trans_datetime=None):
        self.user_id = user_id
        self.datetime = trans_datetime or datetime.datetime.utcnow()
        self.value = value
        self.from_currency = from_currency
        self.from_volume = from_volume
        self.to_currency = to_currency
        self.to_volume = to_volume
        self.stake = stake
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.broker = broker
        self.tx_id = tx_id
        self.notes = notes
