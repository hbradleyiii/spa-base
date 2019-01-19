# -*- coding: utf-8 -*-

"""
app.blueprints.auth.login
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth login manager for spa-base.
"""

from flask_login import LoginManager

from app.models import User


login = LoginManager()

login.login_view = 'auth.login'
login.refresh_view = 'auth.reauthenticate'
login.login_message = u'Please log in to access this page.'
login.session_protection = 'strong'
login.needs_refresh_message = (
    u'To protect your account, please reauthenticate to access this page.'
)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
