# -*- coding: utf-8 -*-

"""
tests.utilities.fixtures
~~~~~~~~~~~~~~~~~~~~~~~~

Fixtures for tests.
"""

import pytest


@pytest.fixture(scope="module")
def app(request):
    """Creates and returns an app with its context."""
    from app import create_app
    from app.config import TestingConfig
    from app.models import db

    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)
    db.create_all()

    return app


@pytest.fixture()
def client(request, app):
    """Creates and returns an app client for testing."""
    client = app.test_client()
    client.__enter__()
    request.addfinalizer(lambda: client.__exit__(None, None, None))
    return client
