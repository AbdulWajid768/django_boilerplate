"""Top-level accounts serializers used by shared utilities."""
from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Lean User serializer returned alongside auth tokens."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
