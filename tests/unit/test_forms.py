# -*- coding: utf-8 -*-

"""
tests.test_forms
~~~~~~~~~~~~~~~~

Unit tests for the main forms module.
"""

import pytest

from app.forms import BaseForm
from app.forms.fields import StringField
from tests.utilities.fixtures import app


def test_form_fields_can_have_an_error_class(app):
    """A form field can have an error class."""
    # Given a form with a field
    class TestForm(BaseForm):
        field = StringField('test field')

    form = TestForm()

    assert form.field(class_='my_class', error_class_='error') == \
            '<input class="my_class" id="field" name="field" type="text" value="">'

    # When the form has errors.
    form.field.errors = True

    # Then you should see the form with the error class
    assert form.field(class_='my_class', error_class_='error') == \
            '<input class="my_class error" id="field" name="field" type="text" value="">'
