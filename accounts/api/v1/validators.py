from rest_framework import serializers

from common.validators import BaseValidator


class LoginValidator(BaseValidator):
    email = serializers.EmailField()
    password = serializers.CharField()
