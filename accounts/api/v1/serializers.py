"""Serializers for accounts v1 APIs."""
from rest_framework import serializers

from accounts.models import Client


class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer for the logged-in client's profile (phone editable, rest read-only)."""

    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'profile_complete']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'profile_complete']
