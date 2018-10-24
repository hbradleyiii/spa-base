# -*- coding: utf-8 -*-

"""
app.models.base
~~~~~~~~~~~~~~~

The db and migrate objects and the BaseModel abstract class for spa-base.

Much of the base model has been derived from:
https://chase-seibert.github.io/blog/2016/03/31/flask-sqlalchemy-sessionless.html
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DatabaseError


db = SQLAlchemy()
session = db.session
migrate = Migrate()


class BaseModel(db.Model):
    __abstract__ = True

    def save(self):
        """Flushes this model to the database (as well as any other pending
        changes)."""
        session.add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        """Updates the model with provided attributes."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        """Deletes this model instance."""
        session.delete(self)
        self._flush()

    def fresh(self):
        """Returns a fresh instance of this model from the database."""
        session.refresh(self)
        return self

    def _flush(self):
        """Flushes any session changes to the database."""
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise
