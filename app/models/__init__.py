# -*- coding: utf-8 -*-

"""
app.models
~~~~~~~~~~

The models module for spa-base.
"""

from sqlalchemy.exc import DatabaseError

from .base import BaseModel, db, IntegrityConstraintViolation, migrate, session
from .user import DuplicateEmailError, Email, User


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)

    @app.after_request
    def session_commit(response):
        """Automatically commit database changes at the end of every successful
        request."""
        if response.status_code >= 400:
            return response
        try:
            session.commit()
            return response
        except DatabaseError:
            session.rollback()
            raise
