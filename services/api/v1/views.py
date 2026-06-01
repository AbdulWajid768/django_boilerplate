"""Services v1 API views."""
from rest_framework.generics import ListAPIView

from services.api.v1.serializers import ServiceSerializer
from services.models import Service


class ServiceListAPIView(ListAPIView):
    """Return all active services ordered by display_order."""

    serializer_class = ServiceSerializer
    pagination_class = None

    def get_queryset(self):
        """Return the active services queryset."""
        return Service.objects.filter(is_active=True)
