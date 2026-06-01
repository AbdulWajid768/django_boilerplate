"""Site content app config (singletons + contact messages)."""
from django.apps import AppConfig


class SiteContentConfig(AppConfig):
    """Default config; wires up signal receivers on ready()."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_content'
    verbose_name = 'Site Content'

    def ready(self):
        """Import signals so contact-form submissions email Maria."""
        from site_content import signals  # noqa: F401
