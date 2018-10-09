# -*- coding: utf-8 -*-

"""
app.mail
~~~~~~~~

The mail module for spa-base.
"""

from flask_mail import Mail, Message


mail = Mail()


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def init_app(app):
    mail.init_app(app)
