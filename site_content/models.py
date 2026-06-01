"""Models for the site_content app: payment instructions, contact messages, site settings."""
from django.db import models

from common.mixins import TimeStampMixin, UUIDPKMixin
from common.singleton import SingletonModel


class PaymentInstruction(SingletonModel, UUIDPKMixin, TimeStampMixin):
    """Singleton holding the bank-transfer details shown to clients during booking."""

    bank_name = models.CharField(max_length=120)
    account_title = models.CharField(max_length=120)
    account_number = models.CharField(max_length=60)
    iban = models.CharField(max_length=60)
    whatsapp_number = models.CharField(max_length=20, help_text='Include country code, e.g. +923001234567')
    payment_note = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Payment instruction'
        verbose_name_plural = 'Payment instructions'

    def __str__(self):
        """Return a recognisable label for admin lists."""
        return f'{self.bank_name} - {self.account_title}'


class ContactMessage(UUIDPKMixin, TimeStampMixin):
    """A message submitted via the public contact form."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact message'
        verbose_name_plural = 'Contact messages'

    def __str__(self):
        """Return a one-line summary for admin lists."""
        return f'{self.name} <{self.email}>'


class SiteSettings(SingletonModel, UUIDPKMixin, TimeStampMixin):
    """Singleton holding home-page stats and the editable About copy."""

    clients_helped = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)
    conditions_treated = models.PositiveIntegerField(default=0)
    sessions_conducted = models.PositiveIntegerField(default=0)
    about_text = models.TextField(blank=True)
    philosophy_quote = models.CharField(max_length=300, blank=True)
    profile_photo = models.ImageField(upload_to='profile/', null=True, blank=True)

    class Meta:
        verbose_name = 'Site setting'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        """Return a static label since only one row exists."""
        return f'Site settings'
