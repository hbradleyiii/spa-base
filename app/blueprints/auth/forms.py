# -*- coding: utf-8 -*-

"""
app.blueprints.auth.forms
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth forms for spa-base.
"""

from flask_wtf.recaptcha import RecaptchaField
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
    recaptcha = RecaptchaField()


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
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('A user with this email has already ' + \
                'registered. Did you forget your password?')
