"""Singleton model base class for site-wide settings rows."""
from django.db import models


class SingletonModel(models.Model):
    """Abstract base ensuring only one row of the subclass ever exists.

    Save() forces the existing PK if any row already exists so the same record is
    re-used; `load()` returns or creates the lone instance.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Force update of the existing singleton row instead of creating new ones."""
        existing = type(self).objects.exclude(pk=self.pk).first()
        if existing is not None:
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the singleton instance, creating an empty one if missing."""
        instance, _ = cls.objects.get_or_create()
        return instance
