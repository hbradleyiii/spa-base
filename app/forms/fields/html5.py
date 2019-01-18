# -*- coding: utf-8 -*-

"""
app.forms.fields.html5
~~~~~~~~~~~~~~~~~~~~~~

WtForms html5 fields extended for spa-base.
"""

from wtforms.fields.html5 import (
    DateField as WtfDateField,
    DateTimeField as WtfDateTimeField,
    DateTimeLocalField as WtfDateTimeLocalField,
    DecimalField as WtfDecimalField,
    DecimalRangeField as WtfDecimalRangeField,
    EmailField as WtfEmailField,
    IntegerField as WtfIntegerField,
    IntegerRangeField as WtfIntegerRangeField,
    SearchField as WtfSearchField,
    TelField as WtfTelField,
    TimeField as WtfTimeField,
    URLField as WtfURLField,
)

from .core import InputMixin


class DateField(InputMixin, WtfDateField):
    """Encapsulates an html5 date field."""

class DateTimeField(InputMixin, WtfDateTimeField):
    """Encapsulates an html5 date/time field."""

class DateTimeLocalField(InputMixin, WtfDateTimeLocalField):
    """Encapsulates an html5 local date/time field."""

class DecimalField(InputMixin, WtfDecimalField):
    """Encapsulates an html5 decimal field."""

class DecimalRangeField(InputMixin, WtfDecimalRangeField):
    """Encapsulates an html5 decimal range field."""

class EmailField(InputMixin, WtfEmailField):
    """Encapsulates an html5 email field."""

class IntegerField(InputMixin, WtfIntegerField):
    """Encapsulates an html5 integer field."""

class IntegerRangeField(InputMixin, WtfIntegerRangeField):
    """Encapsulates an html5 integer range field."""

class SearchField(InputMixin, WtfSearchField):
    """Encapsulates an html5 search field."""

class TelField(InputMixin, WtfTelField):
    """Encapsulates an html5 tel field."""

class TimeField(InputMixin, WtfTimeField):
    """Encapsulates an html5 time field."""

class URLField(InputMixin, WtfURLField):
    """Encapsulates an html5 URL field."""
