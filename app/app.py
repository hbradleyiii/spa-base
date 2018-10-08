# -*- coding: utf-8 -*-

"""
app.app
~~~~~~~

The app factory for spa-base.
"""

from os import path

from dotenv import load_dotenv
from flask import Flask, redirect, request
from werkzeug.utils import find_modules, import_string

from app import models, logger, routes
from .config import Config as DefaultConfig
from .middleware import HTTPMethodOverrideMiddleware


def create_app(Config = None):
    """Flask app factory function."""
    load_dotenv()
    app = Flask(__name__)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    app.config.from_object(Config or DefaultConfig)
    register_blueprints(app)
    models.init_app(app)
    routes.init_app(app)
    logger.init_app(app)

    if app.config['FLASK_ENV'] == 'development':
        # Support static files in development mode
        @app.before_request
        def route_static_files():
            """This function routes static files appropriately when in development
            mode (flask run).

            Rather than forcing all static files to be in the 'static' directory,
            this allows the possiblity of serving files from the root. This is
            quite easy with Apache or Nginx, but when running via `flask run`
            (assuming FLASK_ENV is set to 'development'), this function is
            necessary. It first checks to see if a path is a real file, then it
            redirects to the static soft link which Flask can handle
            appropriately.
            """
            basedir = path.abspath(path.dirname(__file__))
            request_path = request.path
            if request_path[0] == '/':
                request_path = request_path[1:]
            if path.isfile(basedir + '/static/' + request_path):
                return redirect('/static/' + request_path, 307)

        # Shell context for the debug environment
        @app.shell_context_processor
        def make_shell_context():
            from app.models import db, User
            return {'db': db, 'User': User}

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
