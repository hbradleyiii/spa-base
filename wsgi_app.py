# -*- coding: utf-8 -*-

"""
The spa-base wsgi entry point.
"""

from app import create_app


app = create_app()
