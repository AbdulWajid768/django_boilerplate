"""Mixin Classes for Django App."""
import uuid

from django.db import models


class TimeStampMixin(models.Model):
    """Abstract model class to add time related information to model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPKMixin(models.Model):
    """Abstract model that uses a UUID4 primary key instead of the default BigAutoField."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
