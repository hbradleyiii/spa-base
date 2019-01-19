# -*- coding: utf-8 -*-

"""
app.debug
~~~~~~~~~

The app debug module for initializing the debug toolbar and setting up other
helpful debugging utilities. This module is also responsible for properly
handling static files when using `flask run`.
"""

from os import path

from flask import redirect, request, send_file
from flask_debugtoolbar import DebugToolbarExtension


def init_app(app):
    if not app.testing:
        toolbar = DebugToolbarExtension(app)

    # Support static files in development mode
    @app.before_request
    def route_static_files():
        """This function routes static files appropriately when in development
        mode (flask run).

        Rather than forcing all static files to be in the 'static' directory,
        this allows the possiblity of serving files from the root. This is
        quite easy with Apache or Nginx, but when running via `flask run`
        (assuming FLASK_ENV is set to 'development'), this function is
        necessary. It first checks to see if a path is a real file, then it
        redirects to the static soft link which Flask can handle
        appropriately.
        """
        basedir = path.abspath(path.dirname(__file__))
        request_path = request.path
        if request_path[0] == '/':
            request_path = request_path[1:]
        if path.isfile(basedir + '/static/' + request_path):
            return send_file(basedir + '/static/' + request_path)
