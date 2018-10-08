# -*- coding: utf-8 -*-

"""
app.mail
~~~~~~~~

The mail module for spa-base.
"""

from flask_mail import Mail


mail = Mail()


def init_app(app):
    mail.init_app(app)
