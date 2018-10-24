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
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

from .base import BaseModel, db, session


class User(UserMixin, BaseModel):
    __tablename__ = 'users'

    __table_args__ = (
        ForeignKeyConstraint(
            ['primary_email_fk', 'id'],
            ['emails.email', 'emails.user_id'],
            name='fk_user_id_primary_email',
            # Restrict the user from being deleted when attached to a primary
            # email. You must set the primary_email to null first.
            ondelete='RESTRICT',
            use_alter=True
        ),
    )

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    emails = db.relationship('Email', foreign_keys='Email.user_id',
                             cascade='all, delete-orphan',
                             backref='user')
    primary_email_fk = db.Column('primary_email_fk', db.String(128), nullable=True,
                               unique=True)
    primary_email_rel = db.relationship('Email', uselist=False, lazy="joined",
                                    primaryjoin="and_(User.id==Email.user_id, "
                                                "User.primary_email_fk==Email.email)")
    active = db.Column(db.Boolean, default=True)

    def __init__(self, email=None, emails=None, **kwargs):
        if not email and not emails:
            raise ValueError('User must be instantiated with an email.')
        super().__init__(**kwargs)
        self.add_email(email=email, emails=emails)

    def __repr__(self):
        return '<User {} [{}]>'.format(self.name, self.id)

    def __eq__(self, other):
        return isinstance(other, User) and other.id == self.id

    def delete(self):
        """ """
        self.update(primary_email_fk=None)
        super().delete()

    def add_email(self, email=None, emails=None):
        """Adds a single email (or a list of emails) to the user."""
        emails = emails if emails else []
        if email:
            emails.append(email)
        for email in emails:
            self.emails.append(Email(email=email))

    @property
    def name(self):
        """First and last name combined."""
        return self.first_name + ' ' + self.last_name

    @hybrid_property
    def primary_email(self):
        """Attempts to retrieve primary email. If it is none, will attempt to
        get and set the user's first email as primary email."""
        if not self.primary_email_fk:
            email = Email.query.filter_by(user_id=self.id).first()
            if email:
                self.primary_email_fk = email.email
        return self.primary_email_rel

    @primary_email.setter
    def primary_email(self, email):
        self.primary_email_fk = email

    @property
    def password(self):
        """Retrieving the password will only return the hash."""
        return self.password_hash

    @password.setter
    def password(self, password):
        """Setting the password will only set a password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if a provided password matches the stored password_hash."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        """Returns the active state. Useful for semantic conditionals."""
        return self.active

    def avatar(self, size):
        """Returns a url for a gravatar.com avatar based on the user's primary
        email."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @property
    def password_reset_token(self, expires_in=600):
        """Returns a signed password reset token that expires in 'expires_in'
        seconds (defaults to 600)."""
        return jwt_encode({'password_reset': self.email,
                           'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        """Verifies that a provided password reset token is valid."""
        try:
            email = jwt_decode(token, current_app.config['SECRET_KEY'],
                               algorithms=['HS256'])['password_reset']
        except:
            return
        return User.query.join('emails').filter_by(email=email).first()
