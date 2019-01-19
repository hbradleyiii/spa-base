# -*- coding: utf-8 -*-

"""
app.cli
~~~~~~~

The cli tools for spa-base.
"""

import click
import secrets
import os


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
        if os.system('cp assets/icons/*.png htdocs/icons/ && ./node_modules/.bin/pngo htdocs/icons/*.png'):
            raise RuntimeError('"svgo" command failed.')

    @build.command()
    def js():
        """Compiles javascript files."""
        if os.system('./node_modules/.bin/browserify assets/js/app.js -o ./htdocs/js/app.js'):
            raise RuntimeError('"browserify" command failed.')

    @build.command()
    def generate_key():
        """Creates a new randomly generated key."""
        key = secrets.token_hex(24)

        # Ensure env file exists
        with open('./.env', 'a'): pass

        # Load existing contents of ~/.env
        with open('./.env', 'r') as env_file:
            lines = env_file.readlines()

        # Overwrite SECRET_KEY
        for index, line in enumerate(lines):
            if line.startswith('SECRET_KEY='):
                lines[index] = 'SECRET_KEY=' + key + '\n'
                break
        else:
            lines.append('SECRET_KEY=' + key)

        # Save the file
        with open('./.env', 'w') as env_file:
            env_file.writelines(lines)


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
