"""Serializers for appointments v1 APIs."""
from django.utils import timezone
from rest_framework import serializers

from appointments.models import Appointment, AppointmentStatus, AppointmentType
from services.models import Service
from slots.models import AvailableSlot, SlotType


class _SlotSummarySerializer(serializers.ModelSerializer):
    """Nested slot summary used inside Appointment payloads."""

    date = serializers.SerializerMethodField()

    class Meta:
        model = AvailableSlot
        fields = ['id', 'date', 'start_time', 'end_time', 'slot_type']

    def get_date(self, obj):
        """Return the concrete appointment date from the parent appointment."""
        appointment = self.context.get('appointment')
        if appointment and appointment.appointment_date:
            return appointment.appointment_date.isoformat()
        return None


class _ServiceSummarySerializer(serializers.ModelSerializer):
    """Nested service summary used inside Appointment payloads."""

    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'duration_minutes', 'fee_online', 'fee_inperson']


class AppointmentReadSerializer(serializers.ModelSerializer):
    """Outbound serializer returning the public booking record."""

    slot = serializers.SerializerMethodField()
    service = _ServiceSummarySerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'booking_reference',
            'client_name',
            'client_email',
            'client_phone',
            'service',
            'slot',
            'appointment_date',
            'appointment_type',
            'status',
            'client_notes',
            'admin_notes',
            'cancelled_by',
            'cancellation_reason',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_slot(self, obj):
        """Serialize slot with appointment_date injected as slot.date."""
        return _SlotSummarySerializer(
            obj.slot,
            context={'appointment': obj},
        ).data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Inbound serializer for POST /appointments/."""

    service_id = serializers.PrimaryKeyRelatedField(
        source='service',
        queryset=Service.objects.filter(is_active=True),
        write_only=True,
    )
    slot_id = serializers.PrimaryKeyRelatedField(
        source='slot',
        queryset=AvailableSlot.all_objects.all(),
        write_only=True,
    )

    class Meta:
        model = Appointment
        fields = [
            'service_id',
            'slot_id',
            'appointment_date',
            'appointment_type',
            'client_name',
            'client_email',
            'client_phone',
            'client_notes',
        ]

    def validate(self, attrs):
        """Cross-check slot, date, and appointment type compatibility."""
        slot = attrs.get('slot')
        appt_type = attrs.get('appointment_type')
        appt_date = attrs.get('appointment_date')

        if slot.is_deleted:
            raise serializers.ValidationError({'slot_id': 'This slot is no longer available.'})
        if slot.is_disabled:
            raise serializers.ValidationError({'slot_id': 'This slot is unavailable.'})

        if appt_date and appt_date < timezone.localdate():
            raise serializers.ValidationError({'appointment_date': 'Cannot book a date in the past.'})

        if appt_date and slot.weekday != appt_date.weekday():
            raise serializers.ValidationError(
                {'appointment_date': 'This slot is not available on the selected date.'}
            )

        if appt_date and Appointment.objects.filter(
            slot=slot,
            appointment_date=appt_date,
            status__in=[AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED],
        ).exists():
            raise serializers.ValidationError({'slot_id': 'This slot is already booked for that date.'})

        if slot.slot_type == SlotType.ONLINE and appt_type != AppointmentType.ONLINE:
            raise serializers.ValidationError({'appointment_type': 'This slot is online-only.'})
        if slot.slot_type == SlotType.INPERSON and appt_type != AppointmentType.INPERSON:
            raise serializers.ValidationError({'appointment_type': 'This slot is in-person only.'})

        return attrs
