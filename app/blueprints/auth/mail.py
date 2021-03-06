# -*- coding: utf-8 -*-

"""
app.blueprints.auth.email
~~~~~~~~~~~~~~~~~~~~~~~~~

The auth routes for spa-base.
"""

from flask import current_app, render_template
from app.mail import send_mail


def send_email_verification_mail(user, email):
    token = email.verification_token
    send_mail('[SPA-Base] Please Verify Your Email',
              sender=current_app.config['SERVER_EMAIL'], recipients=[str(email)],
              text_body=render_template('auth/email/email_verification.txt',
                                        user=user, token=token),
              html_body=render_template('auth/email/email_verification.html',
                                        user=user, token=token))

def send_password_reset_mail(user):
    token = user.password_reset_token
    send_mail('[SPA-Base] Reset Your Password',
              sender=current_app.config['SERVER_EMAIL'], recipients=[str(user.email)],
              text_body=render_template('auth/email/password_reset.txt',
                                        user=user, token=token),
              html_body=render_template('auth/email/password_reset.html',
                                        user=user, token=token))

def send_email_not_found_mail(email):
    send_mail('[SPA-Base] Email Not Registered',
              sender=current_app.config['SERVER_EMAIL'], recipients=[email],
              text_body=render_template('auth/email/email_not_found.txt'),
              html_body=render_template('auth/email/email_not_found.html'))
