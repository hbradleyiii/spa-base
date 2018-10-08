# -*- coding: utf-8 -*-

"""
app.routes
~~~~~~~~~~

The main routes for spa-base.
"""

from flask import render_template
from flask_login import login_required
from .models import db


def init_app(app):
    """Initializes routes for spa-base."""

    @app.route('/')
    @app.route('/<path:path>')
    @login_required
    def index(path=None):
        return render_template('index.html', path=path)


    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
