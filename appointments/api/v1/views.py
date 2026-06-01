"""Appointments v1 API views."""
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.api.v1.serializers import (
    AppointmentCreateSerializer,
    AppointmentReadSerializer,
)
from appointments.models import Appointment, AppointmentStatus, CancelledBy
from slots.models import AvailableSlot


class AppointmentCreateAPIView(APIView):
    """POST /appointments/ - create a booking (anonymous or authenticated)."""

    def post(self, request):
        """Validate input, lock the slot, create the appointment atomically."""
        serializer = AppointmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slot = serializer.validated_data['slot']
        appointment_date = serializer.validated_data['appointment_date']

        with transaction.atomic():
            locked_slot = AvailableSlot.all_objects.select_for_update().get(pk=slot.id)
            if not locked_slot.is_available_on(appointment_date):
                raise ValidationError({'slot_id': 'This slot is no longer available for that date.'})

            appointment = serializer.save(
                client_user=request.user if request.user.is_authenticated else None,
                status=AppointmentStatus.PENDING,
            )

        return Response(
            AppointmentReadSerializer(appointment).data,
            status=status.HTTP_201_CREATED,
        )


class MyAppointmentsListAPIView(ListAPIView):
    """GET /appointments/mine/ - list logged-in client's bookings."""

    serializer_class = AppointmentReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """Return appointments belonging to the request user, newest date first."""
        queryset = Appointment.objects.filter(
            client_user=self.request.user,
        ).select_related('service', 'slot').order_by('-appointment_date', '-slot__start_time')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset


class MyAppointmentDetailAPIView(RetrieveAPIView):
    """GET /appointments/mine/<booking_reference>/ - single booking detail."""

    serializer_class = AppointmentReadSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_reference'

    def get_queryset(self):
        """Restrict lookup to appointments owned by the request user."""
        return Appointment.objects.filter(client_user=self.request.user).select_related(
            'service', 'slot'
        )


class CancelMyAppointmentAPIView(APIView):
    """POST /appointments/mine/<booking_reference>/cancel/ - client-initiated cancellation."""

    permission_classes = [IsAuthenticated]

    def post(self, request, booking_reference):
        """Cancel a PENDING booking; reject otherwise."""
        appointment = get_object_or_404(
            Appointment.objects.select_related('slot', 'service'),
            booking_reference=booking_reference,
            client_user=request.user,
        )
        if appointment.status != AppointmentStatus.PENDING:
            return Response(
                {'error': f'Cannot cancel an appointment with status {appointment.status}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = AppointmentStatus.CANCELLED
        appointment.cancelled_by = CancelledBy.CLIENT
        appointment.cancellation_reason = request.data.get('reason', '') or ''
        appointment.save()
        return Response(AppointmentReadSerializer(appointment).data)
