"""Serializers for services v1 APIs."""
from rest_framework import serializers

from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Public serializer for the Service catalog."""

    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'short_description',
            'icon',
            'duration_minutes',
            'fee_online',
            'fee_inperson',
            'available_online',
            'available_inperson',
            'display_order',
        ]
        read_only_fields = fields
