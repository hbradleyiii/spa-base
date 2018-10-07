# -*- coding: utf-8 -*-

"""
app.blueprints.auth.login
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth login manager for spa-base.
"""

from flask_login import LoginManager

from app.models import User


login = LoginManager()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
