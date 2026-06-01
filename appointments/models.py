"""Models for the appointments app: bookings with PENDING/CONFIRMED/DECLINED/CANCELLED lifecycle."""
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q

from common.mixins import TimeStampMixin, UUIDPKMixin
from services.models import Service
from slots.models import AvailableSlot


class AppointmentType(models.TextChoices):
    """Whether the consultation is conducted online or in person."""

    ONLINE = 'ONLINE', 'Online'
    INPERSON = 'INPERSON', 'In-person'


class AppointmentStatus(models.TextChoices):
    """Lifecycle status for an Appointment."""

    PENDING = 'PENDING', 'Pending payment'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    DECLINED = 'DECLINED', 'Declined'
    CANCELLED = 'CANCELLED', 'Cancelled'


class CancelledBy(models.TextChoices):
    """Whoever initiated a cancellation."""

    CLIENT = 'CLIENT', 'Client'
    ADMIN = 'ADMIN', 'Admin'


class Appointment(UUIDPKMixin, TimeStampMixin):
    """A booked consultation tied to a weekly slot pattern and a concrete calendar date."""

    booking_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    client_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='appointments',
    )
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='appointments')
    slot = models.ForeignKey(
        AvailableSlot,
        on_delete=models.PROTECT,
        related_name='appointments',
    )
    appointment_date = models.DateField()
    appointment_type = models.CharField(max_length=10, choices=AppointmentType.choices)
    status = models.CharField(
        max_length=10,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
    )
    client_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    cancelled_by = models.CharField(max_length=10, choices=CancelledBy.choices, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-appointment_date', '-slot__start_time']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['slot', 'appointment_date'],
                condition=Q(status__in=['PENDING', 'CONFIRMED']),
                name='unique_active_booking_per_slot_date',
            ),
        ]

    def __str__(self):
        """Return a compact booking summary for admin lists."""
        return f'{self.client_name} - {self.service.name} ({self.status})'
