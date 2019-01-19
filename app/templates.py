# -*- coding: utf-8 -*-

"""
app.templates
~~~~~~~~~~~~~

The app templates module for spa-base.

This file contains the context processors and template filters for the project.
"""

from datetime import datetime


def init_app(app):

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
