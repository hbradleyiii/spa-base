# -*- coding: utf-8 -*-

"""
tests.utilities.client
~~~~~~~~~~~~~~~~~~~~~~

Special flask client for tests.

The idea was derived from:
@see https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
"""

from flask import session as flask_session
from flask.testing import FlaskClient
from flask_wtf.csrf import generate_csrf


class Client(FlaskClient):
    def __init__(self, *args, **kwargs):
        self.application = kwargs.pop('app')
        super(Client, self).__init__(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Automatically injects csrf token into request."""
        if 'data' in kwargs:
            kwargs['data']['csrf_token'] = self.csrf_token
        return super(Client, self).post(*args, **kwargs)

    @property
    def csrf_token(self):
        """Generates a signed csrf token and stores the raw token in the
        current session."""
        with self.session_transaction() as session:
            csrf = generate_csrf()
            session['csrf_token'] = flask_session['csrf_token']
        return csrf
