# -*- coding: utf-8 -*-

"""
app.blueprints.auth
~~~~~~~~~~~~~~~~~~~

The auth blueprint for spa-base.
"""

from .login import login
from .routes import blueprint


def init_app(app):
    login.init_app(app)
