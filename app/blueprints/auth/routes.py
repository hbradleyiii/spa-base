# -*- coding: utf-8 -*-

"""
app.blueprints.auth.routes
~~~~~~~~~~~~~~~~~~~~~~~~~~

The auth routes for spa-base.
"""

from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_user, logout_user
import secrets
from werkzeug.security import check_password_hash
from werkzeug.urls import url_parse

from app.models import db, Email, User
from .forms import (
    LoginForm,
    PasswordResetForm,
    RegistrationForm,
    RequestPasswordResetForm,
)
from .mail import send_email_verification_mail, send_password_reset_mail


blueprint = Blueprint('auth', __name__, template_folder='templates')


def authenticate(user, password):
    """A special authenticate function that helps to prevent timing attacks to
    guess user accounts."""
    if user is None:
        check_password_hash('pbkdf2:sha256:50000$' + secrets.token_hex(8) + '$'
                            + secrets.token_hex(63), secrets.token_hex(13))
        return False
    if not user.check_password(password):
        return False
    return True


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(Email.email==form.email.data).first()
        if not authenticate(user, form.password.data):
            flash('Invalid email address or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login_form.html', title='Login', form=form)


@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        abort(405)
    logout_user()
    return redirect(url_for('auth.login'))


@blueprint.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))
        else:
            flash('There isn\'t a registered user with this email address yet. Would you like to register now?')
            return redirect(url_for('auth.register'))
    return render_template('auth/request_password_reset.html',
                           title='Reset Your Password', form=form)


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', form=form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        send_email_verification_mail(user, user.email)
        flash('Congratulations, you are now a registered user! Please login to continue.')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration_form.html', title='Register',
                           form=form)


@blueprint.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    email = Email.get_email_by_token(token)
    if email:
        email.verify()
        flash('Your email is now verified!')
    else:
        flash('Something went wrong. Please try again.')
    return redirect(url_for('auth.login'))
