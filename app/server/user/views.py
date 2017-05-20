# app/server/user/views.py

from flask import render_template, Blueprint, url_for, redirect, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user

from app.server import bcrypt, db
from app.server.models import User, Account, Transaction, Currency
from app.server.user.forms import LoginForm, RegisterForm, NewAccountForm, NewCurrencyForm, NewTransactionForm

user_blueprint = Blueprint('user', __name__,)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for("user.accounts"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.accounts'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    form = NewAccountForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            currency = Currency.query.filter_by(id=form.currency_code.data.id).first()
            if currency is None:
                abort(400)

            account = Account(user_id=current_user.id, currency_id=currency.id)
            other_account_in_category = Account.query.join(Account.currency).filter(Currency.category == currency.category).first()
            if other_account_in_category is None:
                account.primary_account = True

            db.session.add(account)
            db.session.commit()

            flash('New account for {} ({}) has been created.'.format(currency.code, currency.name), 'success')

        else:
            flash(form.errors, 'danger')

    return render_template('user/accounts.html',
                           form=form,
                           accounts=Account.query.filter_by(user_id=current_user.id).all())


@user_blueprint.route('/currencies')
@login_required
def currencies():
    form = NewCurrencyForm(request.form)
    return render_template('user/currencies.html',
                           form=form,
                           currencies=Currency.query.all())


@user_blueprint.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = NewTransactionForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            value = 100.00
            stake = 0.00
            transaction = Transaction(user_id=current_user.id, value=value, from_currency=form.from_currency.data,
                                      from_volume=form.from_volume.data, to_currency=form.to_currency.data,
                                      to_volume=form.to_volume.data, stake=stake, from_wallet='', to_wallet='',
                                      broker='', tx_id='', notes='')

            db.session.add(transaction)
            db.session.commit()

            flash('New transaction has been logged.', 'success')
        else:
            flash(form.errors, 'danger')

    transactions = Transaction.query.filter_by(user_id=current_user.id)
    return render_template('user/transactions.html',
                           form=form,
                           transactions=transactions)
