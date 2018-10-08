# -*- coding: utf-8 -*-

"""
app.routes
~~~~~~~~~~

The main routes for spa-base.
"""

from flask import render_template
from flask_login import login_required


def init_app(app):
    """Initializes routes for spa-base."""

    @app.route('/')
    @app.route('/<path:path>')
    @login_required
    def index(path=None):
        return render_template('index.html', path=path)
