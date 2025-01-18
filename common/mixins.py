"""Mixin Classes for Django App."""
from django.db import models


class TimeStampMixin(models.Model):
    """Abstract model class to add time related information to model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
