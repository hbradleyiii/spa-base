# -*- coding: utf-8 -*-

"""
app.models
~~~~~~~~~~

The models module for spa-base.
"""


from .base import BaseModel, db, migrate


def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
