# -*- coding: utf-8 -*-

"""
app.debug
~~~~~~~~~

The app debug module for initializing the debug toolbar and other helpful
debugging utilities.
"""

from flask_debugtoolbar import DebugToolbarExtension


toolbar = DebugToolbarExtension()


def init_app(app):
    toolbar.init_app(app)
