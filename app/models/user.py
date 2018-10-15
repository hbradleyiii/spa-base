# -*- coding: utf-8 -*-

"""
app.models.user
~~~~~~~~~~~~~~~

The User model for spa-base.
"""

from flask import current_app
from flask_login import UserMixin
from hashlib import md5
from jwt import encode as jwt_encode, decode as jwt_decode
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseModel, db


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @property
    def password(self):
        """Retrieving the password will only return the hash."""
        return self.password_hash

    @password.setter
    def password(self, password):
        """Setting the password will only set a password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.active

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @property
    def password_reset_token(self, expires_in=600):
        return jwt_encode({'password_reset': self.email,
                           'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        try:
            email = jwt_decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['password_reset']
        except:
            return
        return User.query.filter_by(email=email).first()
