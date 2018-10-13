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
    def test():
        """Runs the unit and feature tests for the app."""
        if os.system('pytest'):
            raise RuntimeError('Tests could not be run.')
