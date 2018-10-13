# -*- coding: utf-8 -*-

"""
flask_app.py
~~~~~~~~~~~~~~

The app entry point for `flask` commands.
"""

from app import cli, create_app
from app.models import db, User


app = create_app()
cli.init_app(app)


@app.shell_context_processor
def make_shell_context():
    """Shell context for the command line environment."""
    return {'db': db, 'User': User}
