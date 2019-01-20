# -*- coding: utf-8 -*-

"""
tests.utilities.fixtures
~~~~~~~~~~~~~~~~~~~~~~~~

Fixtures for tests.
"""

from os import environ

from dotenv import load_dotenv
from flask_migrate import upgrade
import pytest


load_dotenv()


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
    """Creates a new database for each test module.

    When TESTING_USE_MIGRATIONS is set to true, this will also run a fresh
    database migration."""
    from app.models import db

    if environ.get('TESTING_USE_MIGRATIONS', False):
        upgrade('migrations', 'head')
    else:
        db.create_all()

    yield db

    if environ.get('TESTING_USE_MIGRATIONS', False):
        db.engine.execute('DROP TABLE IF EXISTS `alembic_version`;')

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
