# -*- coding: utf-8 -*-

"""
app.cli
~~~~~~~

The cli tools for spa-base.
"""

import os
import click

def init_app(app):

    @app.cli.command()
    @click.option('--mysql/--no-mysql', '-m', default=False)
    def test(mysql):
        """Runs the unit and feature tests for the app."""
        if mysql:
            if os.system('TESTING_USE_DB=True pytest ./tests/'):
                raise RuntimeError('Tests could not be run.')
        else:
            if os.system('pytest ./tests/'):
                raise RuntimeError('Tests could not be run.')
