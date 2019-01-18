# -*- coding: utf-8 -*-

"""
app.forms.fields.core
~~~~~~~~~~~~~~~~~~~~~

WtForms core fields extended for spa-base.

This module includes the InputMixin that allows a special 'error_class_' that
is applied to a field that has errors.
"""

from wtforms.fields.core import (
    BooleanField as WtfBooleanField,
    DecimalField as WtfDecimalField,
    DateField as WtfDateField,
    DateTimeField as WtfDateTimeField,
    FieldList as WtfFieldList,
    FloatField as WtfFloatField,
    FormField as WtfFormField,
    IntegerField as WtfIntegerField,
    RadioField as WtfRadioField,
    SelectField as WtfSelectField,
    SelectMultipleField as WtfSelectMultipleField,
    StringField as WtfStringField,
    TimeField as WtfTimeField,
)


class InputMixin(object):
    """A Mixin to enhance input fields. Specifically, this allows a special
    attribute of 'error_class_' that will be applied as a class to the input
    element if the field has an error."""
    def __call__(self, **kwargs):
        if self.errors and 'error_class_' in kwargs:
            if 'class_' in kwargs:
                kwargs['class_'] = kwargs['class_'] + ' ' + \
                                   kwargs['error_class_']
            else:
                kwargs['class_'] = kwargs['error_class_']
        return super(InputMixin, self).__call__(**kwargs)


class BooleanField(InputMixin, WtfBooleanField):
    """Encapsulates a boolean field."""

class DecimalField(InputMixin, WtfDecimalField):
    """Encapsulates a decimal field."""

class DateField(InputMixin, WtfDateField):
    """Encapsulates a date field."""

class DateTimeField(InputMixin, WtfDateTimeField):
    """Encapsulates a date/time field."""

class FieldList(InputMixin, WtfFieldList):
    """Encapsulates a field list field."""

class FloatField(InputMixin, WtfFloatField):
    """Encapsulates a float field."""

class FormField(InputMixin, WtfFormField):
    """Encapsulates a form field."""

class IntegerField(InputMixin, WtfIntegerField):
    """Encapsulates a integer field."""

class RadioField(InputMixin, WtfRadioField):
    """Encapsulates a radio field."""

class SelectField(InputMixin, WtfSelectField):
    """Encapsulates a select field."""

class SelectMultipleField(InputMixin, WtfSelectMultipleField):
    """Encapsulates a multiple select field."""

class StringField(InputMixin, WtfStringField):
    """Encapsulates a string field."""

class TimeField(InputMixin, WtfTimeField):
    """Encapsulates a time field."""
