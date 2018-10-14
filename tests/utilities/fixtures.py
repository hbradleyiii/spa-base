# -*- coding: utf-8 -*-

"""
tests.utilities.fixtures
~~~~~~~~~~~~~~~~~~~~~~~~

Fixtures for tests.
"""

import pytest


@pytest.fixture(scope='module')
def app(request):
    """Creates and returns an app with its context."""
    from app import create_app
    from app.config import TestingConfig

    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@pytest.fixture(scope='function')
def db(request):
    from app.models import db

    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture()
def client(request, app):
    """Creates and returns an app client for testing."""
    client = app.test_client()
    client.__enter__()
    request.addfinalizer(lambda: client.__exit__(None, None, None))
    return client
