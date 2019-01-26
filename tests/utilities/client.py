# -*- coding: utf-8 -*-

"""
tests.utilities.client
~~~~~~~~~~~~~~~~~~~~~~

Special flask client for tests.

The idea was derived from:
@see https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
"""

from flask import g, url_for
from flask import session as flask_session
from flask.testing import FlaskClient
from flask_wtf.csrf import generate_csrf
from werkzeug.routing import BuildError

from .helpers import create_user


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

    def open(self, path, *args, **kwargs):
        """Wraps the client open method to allow passing flask route strings
        for cleaner test code."""
        path = self.get_url(path)
        return super(Client, self).open(path, *args, **kwargs)

    def get_url(self, string):
        try:
            return url_for(string)
        except BuildError:
            return string

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

    def login(self, email, password):
        return self.post(url_for('auth.login'), data=dict(email='jane@example.com',
                                                          password='password123'))
    def login_new_user(self, session):
        user = create_user(session, password='password123')
        response = self.login(email=user.email, password='password123')
        return user, response
