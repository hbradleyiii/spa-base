# -*- coding: utf-8 -*-

"""
tests.utilities.fixtures
~~~~~~~~~~~~~~~~~~~~~~~~

Fixtures for tests.
"""

import pytest


@pytest.fixture(scope='module')
def app():
    """Creates and returns an app with its context."""
    from app import create_app
    from app.config import TestingConfig

    app = create_app(TestingConfig)
    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='module')
def db(app):
    """Creates a new database for each test module."""
    from app.models import db

    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Creates a new database session for a test.
    @see http://alexmic.net/flask-sqlalchemy-pytest/"""
    connection = db.engine.connect()
    transaction = connection.begin()
    db.session.configure(bind=connection, binds={})

    yield db.session

    transaction.rollback()
    connection.close()
    db.session.remove()


@pytest.fixture()
def client(app):
    """Creates and returns an app client for testing."""
    client = app.test_client()
    client.__enter__()

    yield client

    client.__exit__(None, None, None)
