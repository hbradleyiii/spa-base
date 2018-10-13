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

# Shell context for the command line environment
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
