# -*- coding: utf-8 -*-

"""
app.config
~~~~~~~~~~

The app config for spa-base.
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """The default config object."""
    FLASK_ENV                = os.environ.get('FLASK_ENV') or 'production'
    DEBUG                    = os.environ.get('DEBUG') or False
    TESTING                  = os.environ.get('TESTING') or False
    SECRET_KEY               = os.environ.get('SECRET_KEY') or \
                               '___change_me_please___'

    SESSION_COOKIE_DOMAIN    = os.environ.get('SESSION_COOKIE_DOMAIN') or None
    SESSION_COOKIE_HTTPONLY  = os.environ.get('SESSION_COOKIE_HTTPONLY') or True
    SESSION_COOKIE_NAME      = os.environ.get('SESSION_COOKIE_NAME') or 'session'
    SESSION_COOKIE_PATH      = os.environ.get('SESSION_COOKIE_PATH') or None
    SESSION_COOKIE_SAMESITE  = os.environ.get('SESSION_COOKIE_SAMESITE') or None
    SESSION_COOKIE_SECURE    = os.environ.get('SESSION_COOKIE_SECURE') or False

    SQLALCHEMY_DATABASE_URI  = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir + '/../', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME            = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD            = os.environ.get('MAIL_PASSWORD') or None
    MAIL_SERVER              = os.environ.get('MAIL_SERVER') or None
    MAIL_PORT                = int(os.environ.get('MAIL_PORT')) or 443
    MAIL_USE_TLS             = os.environ.get('MAIL_USE_TLS') is not None or True
    ADMIN_EMAILS             = os.environ.get('ADMIN_EMAILS').split(',') or []
    SERVER_EMAIL             = os.environ.get('SERVER_EMAIL') or None


class TestingConfig(Config):
    """The testing config object."""
    TESTING = True
