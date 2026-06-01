"""Models for the slots app: weekly recurring bookable time patterns."""
from django.db import models
from django.db.models import Q

from common.mixins import TimeStampMixin, UUIDPKMixin


class SlotType(models.TextChoices):
    """Allowed slot delivery types (mirrors Appointment.appointment_type plus a BOTH)."""

    ONLINE = 'ONLINE', 'Online'
    INPERSON = 'INPERSON', 'In-person'
    BOTH = 'BOTH', 'Online or In-person'


class Weekday(models.IntegerChoices):
    """ISO weekday index matching Python date.weekday() (Monday=0)."""

    MONDAY = 0, 'Monday'
    TUESDAY = 1, 'Tuesday'
    WEDNESDAY = 2, 'Wednesday'
    THURSDAY = 3, 'Thursday'
    FRIDAY = 4, 'Friday'
    SATURDAY = 5, 'Saturday'
    SUNDAY = 6, 'Sunday'


class AvailableSlotQuerySet(models.QuerySet):
    """QuerySet helpers for weekly slot availability."""

    def active(self):
        """Return slots that are not soft-deleted."""
        return self.filter(is_deleted=False)

    def for_weekday(self, weekday):
        """Return active slots matching the given weekday index."""
        return self.active().filter(weekday=weekday, is_disabled=False)

    def available_for_date(self, target_date, slot_type=None):
        """Return bookable slots on a calendar date (weekday match, not taken)."""
        from appointments.models import Appointment, AppointmentStatus

        qs = self.for_weekday(target_date.weekday())
        if slot_type:
            if slot_type == SlotType.BOTH:
                pass
            else:
                qs = qs.filter(Q(slot_type=slot_type) | Q(slot_type=SlotType.BOTH))

        taken_ids = Appointment.objects.filter(
            appointment_date=target_date,
            status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED],
        ).values_list('slot_id', flat=True)
        return qs.exclude(id__in=taken_ids)


class AvailableSlotManager(models.Manager):
    """Default manager excluding soft-deleted rows."""

    def get_queryset(self):
        """Exclude soft-deleted slots from the default queryset."""
        return AvailableSlotQuerySet(self.model, using=self._db).active()

    def available_for_date(self, target_date, slot_type=None):
        """Return slots bookable on the given calendar date."""
        return self.get_queryset().available_for_date(target_date, slot_type)

    def including_deleted(self):
        """Return all rows including soft-deleted (for admin)."""
        return AvailableSlotQuerySet(self.model, using=self._db)


class AvailableSlot(UUIDPKMixin, TimeStampMixin):
    """A weekly recurring time pattern clients can book on matching calendar dates."""

    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_type = models.CharField(max_length=10, choices=SlotType.choices, default=SlotType.BOTH)
    is_disabled = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)

    objects = AvailableSlotManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['weekday', 'start_time']
        verbose_name = 'Available slot'
        verbose_name_plural = 'Available slots'
        constraints = [
            models.UniqueConstraint(
                fields=['weekday', 'start_time', 'slot_type'],
                name='unique_slot_per_weekday_time_type',
            ),
        ]

    def __str__(self):
        """Return a compact representation of the slot for admin lists."""
        weekday_label = self.get_weekday_display()
        return f'{weekday_label} {self.start_time:%H:%M} ({self.get_slot_type_display()})'

    def is_available_on(self, target_date):
        """Whether this slot can be booked on the given calendar date."""
        from appointments.models import Appointment, AppointmentStatus

        if self.is_deleted or self.is_disabled:
            return False
        if target_date.weekday() != self.weekday:
            return False
        return not Appointment.objects.filter(
            slot=self,
            appointment_date=target_date,
            status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED],
        ).exists()
