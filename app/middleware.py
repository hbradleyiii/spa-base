# -*- coding: utf-8 -*-

"""
app.middleware
~~~~~~~~~~~~~~

This module contains the flask middleware for the application.
"""


class HTTPMethodOverrideMiddleware(object):
    """Many servers do not allow newer HTTP methods (such as PATCH, PUT, etc).
    This middleware allows "proxied" HTTP methods using a POST request and
    setting the X-HTTP-Method-Override header to the intended HTTP method.

    @see http://flask.pocoo.org/docs/1.0/patterns/methodoverrides/
    """
    allowed_methods = frozenset([
        'GET',
        'HEAD',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    ])
    bodyless_methods = frozenset(['GET', 'HEAD', 'OPTIONS', 'DELETE'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
