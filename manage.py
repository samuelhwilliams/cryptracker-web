#!/usr/bin/env python3.6

import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*',
        'app/server/config.py',
        'app/server/*/__init__.py'
    ]
)
COV.start()

from app.server import app, db
from app.server.models import User, Currency, CurrencyCategory


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    db.session.add(Currency(CurrencyCategory.Fiat, 'GBP', 'Great British Pound'))
    db.session.add(Currency(CurrencyCategory.Fiat, 'EUR', 'Euro'))
    db.session.add(Currency(CurrencyCategory.Fiat, 'USD', 'United States Dollar'))

    db.session.add(Currency(CurrencyCategory.Crypto, 'BTC', 'Bitcoin'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'LTC', 'Litecoin'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'SC', 'Siacoin'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'XRP', 'Ripple'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'DGB', 'DigiByte'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'XMR', 'Monero'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'ETH', 'Ethereum'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'STORJ', 'Storj'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'XEM', 'NEM'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'GNT', 'Golem'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'XLM', 'Stellar Lumen'))
    db.session.add(Currency(CurrencyCategory.Crypto, 'NXT', 'Nxt'))

    db.session.commit()

@manager.command
def seed():
    create_db()
    create_admin()
    create_data()


if __name__ == '__main__':
    manager.run()
