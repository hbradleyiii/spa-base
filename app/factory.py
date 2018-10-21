# -*- coding: utf-8 -*-

"""
app.factory
~~~~~~~~~~~

The app factory for spa-base.
"""

from flask import Flask
from werkzeug.utils import find_modules, import_string

from app import (
    debug,
    logger,
    mail,
    models,
    routes,
)
from .config import Config as DefaultConfig, DebugConfig
from .middleware import HTTPMethodOverrideMiddleware


def create_app(Config = None):
    """Flask app factory function."""
    app = Flask(__name__)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    if not Config:
        Config = DefaultConfig if not app.debug else DebugConfig
    app.config.from_object(Config)
    register_blueprints(app)
    models.init_app(app)
    routes.init_app(app)
    mail.init_app(app)

    if not app.testing:
        logger.init_app(app)

    if app.debug:
        debug.init_app(app)

    return app


def register_blueprints(app):
    """Automatically registers all blueprints that are in the app.blueprints
    package.

    @see https://speakerdeck.com/player/94a53afb6a524ad88f301f62166a27e4
    """
    for name in find_modules('app.blueprints', include_packages=True,
                             recursive=True):
        bp = import_string(name)
        if hasattr(bp, 'blueprint'):
            app.register_blueprint(bp.blueprint)
        if hasattr(bp, 'init_app'):
            bp.init_app(app)
