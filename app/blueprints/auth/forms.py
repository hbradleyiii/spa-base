# -*- coding: utf-8 -*-

"""
app.blueprints.auth.forms
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth forms for spa-base.
"""

from wtforms.fields import (
    BooleanField,
    PasswordField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
)

from app.forms import BaseForm


class LoginForm(BaseForm):
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
