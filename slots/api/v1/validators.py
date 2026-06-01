"""Validators for slots v1 APIs."""
from datetime import datetime

from rest_framework import serializers

from common.validators import BaseValidator
from slots.models import SlotType


class SlotListValidator(BaseValidator):
    """Validate the `date` and `type` query params for GET /slots/."""

    date = serializers.DateField()
    type = serializers.ChoiceField(
        choices=SlotType.choices,
        required=False,
        allow_blank=True,
    )


class AvailableDatesValidator(BaseValidator):
    """Validate the `month` (YYYY-MM) and `type` query params for available-dates lookup."""

    month = serializers.CharField()
    type = serializers.ChoiceField(
        choices=SlotType.choices,
        required=False,
        allow_blank=True,
    )

    def validate_month(self, value):
        """Ensure month is in YYYY-MM format and return a (year, month) tuple."""
        try:
            parsed = datetime.strptime(value, '%Y-%m')
        except ValueError as exc:
            raise serializers.ValidationError(f'Expected YYYY-MM, got "{value}".') from exc
        return parsed.year, parsed.month
