# -*- coding: utf-8 -*-

"""
app.forms.fields.simple
~~~~~~~~~~~~~~~~~~~~~~~

WtForms simple fields extended for spa-base.
"""

from wtforms.fields.simple import (
    TextAreaField as WtfTextAreaField,
    PasswordField as WtfPasswordField,
    FileField as WtfFileField,
    MultipleFileField as WtfMultipleField,
    HiddenField as WtfHiddenField,
    SubmitField as WtfSubmitField,
)

from .core import InputMixin


class TextAreaField(InputMixin, WtfTextAreaField):
	"""Encapsulates a text area field."""

class PasswordField(InputMixin, WtfPasswordField):
	"""Encapsulates a password field."""

class FileField(InputMixin, WtfFileField):
	"""Encapsulates a file field."""

class MultipleFileField(InputMixin, WtfMultipleField):
	"""Encapsulates a multiple file field."""

class HiddenField(InputMixin, WtfHiddenField):
	"""Encapsulates a hidden field."""

class SubmitField(InputMixin, WtfSubmitField):
	"""Encapsulates a submit button field."""
