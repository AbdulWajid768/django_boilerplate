"""Site_content v1 API views."""
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from site_content.api.v1.serializers import (
    ContactMessageCreateSerializer,
    PaymentInstructionSerializer,
    SiteSettingsSerializer,
)
from site_content.models import PaymentInstruction, SiteSettings


class PaymentInstructionAPIView(APIView):
    """Return the singleton PaymentInstruction record."""

    def get(self, request):
        """Return the singleton's payload (empty fields if not yet seeded)."""
        instance = PaymentInstruction.load()
        return Response(PaymentInstructionSerializer(instance).data)


class SiteSettingsAPIView(APIView):
    """Return the singleton SiteSettings record."""

    def get(self, request):
        """Return the singleton's payload (empty fields if not yet seeded)."""
        instance = SiteSettings.load()
        return Response(SiteSettingsSerializer(instance, context={'request': request}).data)


class ContactMessageCreateAPIView(CreateAPIView):
    """POST /contact/ - public contact form submission."""

    serializer_class = ContactMessageCreateSerializer

    def create(self, request, *args, **kwargs):
        """Create the message and return a minimal success payload."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'success': True, 'message': 'Thanks for reaching out. Maria will get back to you soon.'},
            status=status.HTTP_201_CREATED,
        )
