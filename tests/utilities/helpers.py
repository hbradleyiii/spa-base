# -*- coding: utf-8 -*-

"""
tests.utilities.helpers
~~~~~~~~~~~~~~~~~~~~~~~

Helper functions for tests.
"""

from app.models import User


def create_user(db, first_name='Jane', last_name='Doe', password='password123',
                email='jane@example.com', emails=[]):
    """Helper function to create a user for the app."""
    user = User(first_name=first_name, last_name=last_name, password=password,
                email=email, emails=emails)
    db.session.add(user)
    db.session.commit()
    return user
