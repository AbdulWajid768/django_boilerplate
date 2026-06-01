"""Slots v1 API views."""
from datetime import date, timedelta

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import apply_validation
from slots.api.v1.serializers import AvailableSlotSerializer
from slots.api.v1.validators import AvailableDatesValidator, SlotListValidator
from slots.models import AvailableSlot


class AvailableSlotListAPIView(ListAPIView):
    """List bookable slots for a given date (optionally filtered by type)."""

    serializer_class = AvailableSlotSerializer
    pagination_class = None

    def get_queryset(self):
        """Return weekly slots available on the requested calendar date."""
        validator = apply_validation(SlotListValidator, self.request.query_params)
        params = validator.validated_data
        return AvailableSlot.objects.available_for_date(
            params['date'],
            params.get('type'),
        )

    def get_serializer_context(self):
        """Pass the requested date into the serializer for the injected date field."""
        context = super().get_serializer_context()
        validator = apply_validation(SlotListValidator, self.request.query_params)
        context['target_date'] = validator.validated_data['date']
        return context


class AvailableDatesAPIView(APIView):
    """Return the set of dates within a month that have at least one available slot."""

    def get(self, request):
        """Return list of ISO date strings with at least one bookable slot."""
        validator = apply_validation(AvailableDatesValidator, request.query_params)
        year, month = validator.validated_data['month']
        requested_type = validator.validated_data.get('type')

        first = date(year, month, 1)
        if month == 12:
            last = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last = date(year, month + 1, 1) - timedelta(days=1)

        available_dates = []
        current = first
        while current <= last:
            if AvailableSlot.objects.available_for_date(current, requested_type).exists():
                available_dates.append(current.isoformat())
            current += timedelta(days=1)

        return Response({'dates': available_dates})
