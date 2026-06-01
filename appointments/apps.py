"""Appointments app config."""
from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Default config; wires up signal receivers on ready()."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        """Import signals so email notifications fire on new bookings."""
        from appointments import signals  # noqa: F401
