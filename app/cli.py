# -*- coding: utf-8 -*-

"""
app.cli
~~~~~~~

The cli tools for spa-base.
"""

import os
import click

def init_app(app):

    @app.cli.group()
    def build():
        """Runs the build commands for the app."""
        pass

    @build.command()
    def sass():
        """Compiles sass files."""
        if os.system('sassc -I ./node_modules/bulma assets/sass/app.scss htdocs/css/app.css'):
            raise RuntimeError('"sassc" command failed.')
        if os.system('sassc -I ./node_modules/bulma assets/sass/auth.scss htdocs/css/auth.css'):
            raise RuntimeError('"sassc" command failed.')

    @build.command()
    def icons():
        """Compresses icon svgs."""
        if os.system('./node_modules/.bin/svgo --config=./.svgo.yml assets/icons/*.svg -o htdocs/icons/'):
            raise RuntimeError('"svgo" command failed.')

    @build.command()
    def js():
        """Compiles javascript files."""
        if os.system('./node_modules/.bin/browserify assets/js/app.js -o ./htdocs/js/app.js'):
            raise RuntimeError('"browserify" command failed.')

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
