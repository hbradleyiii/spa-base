# -*- coding: utf-8 -*-

"""
app.blueprints.auth.forms
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth forms for spa-base.
"""

from flask_wtf.recaptcha import RecaptchaField
from flask_wtf.recaptcha.validators import Recaptcha
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
)

from app.forms import BaseForm
from app.forms.fields import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from app.models import User


class LoginForm(BaseForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestPasswordResetForm(BaseForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    recaptcha = RecaptchaField(validators=[
                               Recaptcha('Please click this box to show you are not a bot.')])


class PasswordResetForm(BaseForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                     EqualTo('password')])
    submit = SubmitField('Change Password')


class RegistrationForm(BaseForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    recaptcha = RecaptchaField(validators=[
                               Recaptcha('Please click this box to show you are not a bot.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('A user with this email has already ' + \
                'registered. Did you forget your password?')
