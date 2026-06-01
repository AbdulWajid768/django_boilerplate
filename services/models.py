"""Models for the services app: catalog of consultation services Maria offers."""
from django.db import models

from common.mixins import TimeStampMixin, UUIDPKMixin


class Service(UUIDPKMixin, TimeStampMixin):
    """A consultation service the practitioner offers (e.g. Weight Management)."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, blank=True)
    duration_minutes = models.PositiveIntegerField()
    fee_online = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fee_inperson = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_online = models.BooleanField(default=True)
    available_inperson = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        """Return the service name for admin readability."""
        return f'{self.name}'
