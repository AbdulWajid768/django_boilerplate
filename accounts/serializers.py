from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for handling user actions."""

    class Meta:
        model = User
        fields = [ 'id', 'email', 'first_name', 'last_name']
