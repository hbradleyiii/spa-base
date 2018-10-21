# -*- coding: utf-8 -*-

"""
tests.utilities.decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorators for tests.
"""

from os import environ
from warnings import warn

from dotenv import load_dotenv


load_dotenv()

def requires_mysql(fn):
    def skip(*args, **kwargs):
        pass
    if environ.get('TESTING_USE_DB', False) and \
       'mysql://' in environ.get('TEST_DATABASE_URI', ''):
        return fn
    else:
        warn('Test "' + fn.__name__ + '" skipped because it requires a MySQL database to run correctly.')
        return skip
