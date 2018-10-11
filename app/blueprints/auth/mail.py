# -*- coding: utf-8 -*-

"""
app.blueprints.auth.email
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth routes for spa-base.
"""

from flask import current_app, render_template
from app.mail import send_mail


def send_password_reset_mail(user):
    token = user.password_reset_token
    send_mail('[SPA-Base] Reset Your Password',
              sender=current_app.config['SERVER_EMAIL'], recipients=[user.email],
              text_body=render_template('auth/email/password_reset.txt', user=user, token=token),
              html_body=render_template('auth/email/password_reset.html',
                                        user=user, token=token))
