# -*- coding: utf-8 -*-

"""
tests.utilities.client
~~~~~~~~~~~~~~~~~~~~~~

Special flask client for tests.

The idea was derived from:
@see https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
"""

from flask import g
from flask import session as flask_session
from flask.testing import FlaskClient
from flask_wtf.csrf import generate_csrf


class Client(FlaskClient):
    def __init__(self, *args, **kwargs):
        self.application = kwargs.pop('app')
        super(Client, self).__init__(*args, **kwargs)
        self.csrf_token = self.generate_csrf()

    def post(self, *args, **kwargs):
        """Automatically injects csrf token into request."""
        if 'data' in kwargs:
            kwargs['data']['csrf_token'] = self.csrf_token
        return super(Client, self).post(*args, **kwargs)

    def generate_csrf(self):
        """Generates a signed csrf token and stores the raw token in the
        current session."""
        with self.session_transaction() as session:
            # Remove the previous session's token if there is one
            if 'csrf_token' in g:
                g.pop('csrf_token')
            csrf = generate_csrf()
            session['csrf_token'] = flask_session['csrf_token']
        return csrf
