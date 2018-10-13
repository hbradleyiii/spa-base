# -*- coding: utf-8 -*-

"""
flask_app.py
~~~~~~~~~~~~~~

The app entry point for `flask` commands.
"""

from app import cli, create_app


app = create_app()
cli.init_app(app)
