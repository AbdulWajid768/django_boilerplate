"""Validation related class and functions for Django App."""
from rest_framework import serializers


class BaseValidator(serializers.Serializer):
    """Parent class for validation serializers that override abstract requires methods."""

    def create(self, validated_data):
        """Empty override of serializer create method."""

    def update(self, instance, validated_data):
        """Empty override of serializer update method."""
