from django import forms
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy


class URLTextField(models.TextField):
    """ Same as django.db.models.URLField but without a character limit """
    default_validators = [validators.URLValidator()]
    description = gettext_lazy("URL")

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': forms.URLField,
            **kwargs,
        })
