"""Slots app config."""
from django.apps import AppConfig


class SlotsConfig(AppConfig):
    """Default config for the slots app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slots'
