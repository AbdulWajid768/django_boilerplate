"""Serializers for slots v1 APIs."""
from datetime import datetime, timedelta

from rest_framework import serializers

from slots.models import AvailableSlot


class AvailableSlotSerializer(serializers.ModelSerializer):
    """Public serializer used to list bookable slots for a calendar date."""

    date = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = AvailableSlot
        fields = [
            'id',
            'date',
            'start_time',
            'end_time',
            'slot_type',
            'duration_minutes',
        ]
        read_only_fields = fields

    def get_date(self, obj):
        """Inject the requested calendar date from serializer context."""
        return self.context.get('target_date')

    def get_duration_minutes(self, obj):
        """Compute slot length in minutes from start/end time."""
        target_date = self.context.get('target_date')
        if not target_date:
            return None
        start = datetime.combine(target_date, obj.start_time)
        end = datetime.combine(target_date, obj.end_time)
        if end < start:
            end += timedelta(days=1)
        return int((end - start).total_seconds() // 60)
