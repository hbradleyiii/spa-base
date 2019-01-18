# -*- coding: utf-8 -*-

"""
app.forms.fields
~~~~~~~~~~~~~~~~

The form fields module for spa-base.
"""

from .core import (
    BooleanField,
    FieldList,
    FloatField,
    FormField,
    RadioField,
    SelectField,
    SelectMultipleField,
    StringField,
)

from .simple import (
    TextAreaField,
    PasswordField,
    FileField,
    MultipleFileField,
    HiddenField,
    SubmitField,
)

from .html5 import (
    DateField,
    DateTimeField,
    DateTimeLocalField,
    DecimalField,
    DecimalRangeField,
    EmailField,
    IntegerField,
    IntegerRangeField,
    SearchField,
    TelField,
    TimeField,
    URLField,
)
