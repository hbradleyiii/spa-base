# -*- coding: utf-8 -*-

"""
app.mail
~~~~~~~~

The mail module for spa-base.
"""

from threading import Thread

from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


def send_mail(subject, sender, recipients, text_body, html_body,
              send_async=True):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if send_async:
        Thread(target=send_mail_async, args=(current_app._get_current_object(),
                                             msg)).start()
    else:
        mail.send(msg)


def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)


def init_app(app):
    mail.init_app(app)
