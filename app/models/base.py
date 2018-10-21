# -*- coding: utf-8 -*-

"""
app.models.base
~~~~~~~~~~~~~~~

The db and migrate objects and the BaseModel abstract class for spa-base.
"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class BaseModel(db.Model):
    __abstract__ = True

    def delete(self):
        """Deletes this model instance."""
        db.session.delete(self)
        db.session.commit()
