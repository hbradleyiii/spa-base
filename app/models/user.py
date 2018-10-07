# -*- coding: utf-8 -*-

"""
app.models
~~~~~~~~~~

The models module for spa-base.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseModel, db


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True,
                         nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

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
