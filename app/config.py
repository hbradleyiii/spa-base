# -*- coding: utf-8 -*-

"""
app.config
~~~~~~~~~~

The app config for spa-base.
"""

from os import environ, path


basedir = path.abspath(path.dirname(__file__))


def _is_true(env_var):
	return env_var.lower() in [1, 'true', 'yes']


class Config(object):
    """The default config object."""
    FLASK_ENV                = environ.get('FLASK_ENV', 'production')
    DEBUG                    = _is_true(environ.get('DEBUG', 'false'))
    TESTIN                   = _is_true(environ.get('TESTING', 'false'))
    SECRET_KEY               = environ.get('SECRET_KEY', '___change_me_please___')

    SESSION_COOKIE_DOMAIN    = environ.get('SESSION_COOKIE_DOMAIN', None)
    SESSION_COOKIE_HTTPONLY  = _is_true(environ.get('SESSION_COOKIE_HTTPONLY', 'false'))
    SESSION_COOKIE_NAME      = environ.get('SESSION_COOKIE_NAME', 'session')
    SESSION_COOKIE_PATH      = environ.get('SESSION_COOKIE_PATH', None)
    SESSION_COOKIE_SAMESITE  = environ.get('SESSION_COOKIE_SAMESITE', None)
    SESSION_COOKIE_SECURE    = _is_true(environ.get('SESSION_COOKIE_SECURE', 'false'))

    SQLALCHEMY_DATABASE_URI  = environ.get('DATABASE_URL',
        'sqlite:///' + path.join(basedir + '/../', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME            = environ.get('MAIL_USERNAME', None)
    MAIL_PASSWORD            = environ.get('MAIL_PASSWORD', None)
    MAIL_SERVER              = environ.get('MAIL_SERVER', None)
    MAIL_PORT                = int(environ.get('MAIL_PORT', 443))
    MAIL_USE_TLS             = _is_true(environ.get('MAIL_USE_TLS', 'True'))
    ADMIN_EMAILS             = environ.get('ADMIN_EMAILS', '').split(',')
    SERVER_EMAIL             = environ.get('SERVER_EMAIL', None)

    LOG_LEVEL                = environ.get('LOG_LEVEL', 'INFO')
    MAIL_LOG_LEVEL           = environ.get('MAIL_LOG_LEVEL', 'ERROR')


class TestingConfig(Config):
    """The testing config object."""
    TESTING = True
