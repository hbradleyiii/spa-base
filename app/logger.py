# -*- coding: utf-8 -*-

"""
app.logger
~~~~~~~~~~

The logger module for spa-base.
"""

import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from os import mkdir, path


def initialize_mail_on_error(app):
    if not app.config['MAIL_SERVER']:
        return # Can't do anything if MAIL_SERVER is not set

    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['SERVER_EMAIL'],
        toaddrs=app.config['ADMIN_EMAILS'], subject='SPA-base Failure',
        credentials=auth, secure=secure)
    mail_handler.setLevel(getattr(logging, app.config['MAIL_LOG_LEVEL']))
    app.logger.addHandler(mail_handler)


def initialize_log_on_error(app):
    if not path.exists('logs'):
        mkdir('logs')
    file_handler = RotatingFileHandler('logs/flask.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info('Microblog startup')


def init_app(app):
    """Initializes error logging."""
    if app.debug:
        return # Do nothing if we are in debug mode

    initialize_mail_on_error(app)
    initialize_log_on_error(app)
