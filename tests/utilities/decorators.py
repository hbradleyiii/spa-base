# -*- coding: utf-8 -*-

"""
tests.utilities.decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorators for tests.

Assumes fixtures are being loaded and load_dotenv() has been called.
"""

from os import environ
from warnings import warn


def requires_mysql(fn):
    def skip(*args, **kwargs):
        pass
    if environ.get('TESTING_USE_DB', False) and \
       'mysql://' in environ.get('TEST_DATABASE_URI', ''):
        return fn
    else:
        warn('Test "' + fn.__name__ + '" skipped because it requires a MySQL database to run correctly.')
        return skip
