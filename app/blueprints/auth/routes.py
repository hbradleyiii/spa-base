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
    ChangeEmailForm,
    LoginForm,
    PasswordResetForm,
    RegistrationForm,
    RequestPasswordResetForm,
)
from .mail import (
    send_email_not_found_mail,
    send_email_verification_mail,
    send_password_reset_mail,
)


blueprint = Blueprint('auth', __name__, template_folder='templates')


def authenticate(user, password):
    """A special authenticate function that helps to prevent timing attacks to
    guess user accounts."""
    fake_hash = 'pbkdf2:sha256:50000$' + secrets.token_hex(8) + '$' \
                + secrets.token_hex(63)
    fake_password = secrets.token_hex(13)
    if user is None:
        check_password_hash(fake_hash, fake_password)
        return False
    return user.check_password(password)


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(Email.email==form.email.data).first()
        if not authenticate(user, form.password.data):
            flash('Invalid email address or password')
            return render_template('auth/login_form.html', title='Login', form=form)
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
        email = Email.query.filter_by(email=form.email.data).first()
        if email:
            send_password_reset_mail(email.user)
        else:
            send_email_not_found_mail(form.email.data)
        flash('Check your email for instructions to reset your password or to'
              ' register for an account if you don\'t already have one.')
        return redirect(url_for('auth.login'))
    return render_template('auth/request_password_reset.html',
                           title='Reset Your Password', form=form)


@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def password_reset(token):
    user = User.verify_password_reset_token(token)
    if not user:
        return redirect(url_for('auth.request_password_reset'))
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
        user.save()
        login_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.send_email_verification'))
    return render_template('auth/registration_form.html', title='Register',
                           form=form)


@blueprint.route('/send_email_verification/', methods=['GET'])
@blueprint.route('/send_email_verification/<email>', methods=['GET'])
def send_email_verification(email=None):
    if not current_user.is_authenticated:
        flash('You must log in before you can verify your email.')
        return redirect(url_for('auth.login',
                                next=url_for('auth.send_email_verification')))
    if not email:
        email = current_user.email
    else:
        email = Email.query.filter_by(email=email, user_id=current_user.id).first()

    if not email or email.is_verified:
        return redirect(url_for('index'))
    send_email_verification_mail(current_user, email)
    return render_template('auth/send_email_verification.html',
                           title='Please Confirm Your Email',
                           email=email)


@blueprint.route('/change_email/', methods=['GET', 'POST'])
def change_email():
    if not current_user.is_authenticated:
        flash('You must log in before you can change your email.')
        return redirect(url_for('auth.login',
                                next=url_for('auth.change_email')))
    form = ChangeEmailForm()
    if form.validate_on_submit():
        old_email = current_user.email
        current_user.add_email(form.email.data)
        current_user.save()
        old_email.delete()
        return redirect(url_for('auth.send_email_verification'))
    return render_template('auth/change_email.html', title='Register',
                           form=form, user=current_user)


@blueprint.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    email = Email.get_email_by_token(token)
    if email:
        email.verify()
        flash('Your email is now verified!')
    else:
        flash('Something went wrong. Please try again.')
    return redirect(url_for('auth.login'))
