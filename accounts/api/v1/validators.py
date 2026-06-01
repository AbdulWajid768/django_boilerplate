"""Validators for accounts v1 APIs."""
from rest_framework import serializers

from common.validators import BaseValidator


class GoogleLoginValidator(BaseValidator):
    """Validate the inbound Google id_token payload."""

    id_token = serializers.CharField()
