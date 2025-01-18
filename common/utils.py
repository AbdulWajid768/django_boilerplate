"""Utility functions for Django App."""
import base64
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError


def apply_validation(serializer_class, data, raise_exception=True):
    """Apply validation via serializer class on provided data."""
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=raise_exception)
    return serializer


def get_object_or_none(model_class, **kwargs):
    """Return object if exists else None."""
    try:
        return model_class.objects.get(**kwargs)
    except (model_class.DoesNotExist, TypeError, ValueError, ValidationError):
        return None


def get_absolute_media_url(url):
    """Return absolute url of provided url."""
    return f'{settings.BASE_URL}{url}'


def time_string_to_seconds(time_string):
    """Convert time string to seconds."""
    try:
        time_obj = datetime.strptime(time_string, "%H:%M:%S.%f")
    except ValueError:
        time_obj = datetime.strptime(time_string, "%H:%M:%S")
    return round(time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1_000_000)


def decode_into_base64_data(data):
    """Decode data into base64 string."""
    return base64.b64decode(data).decode('utf-8')


def encode_into_base64_data(data):
    """Encode data into base64 string."""
    return base64.b64encode(data)


def update_instance(instance, **fields):
    """Utility to update specified fields of the instance."""
    for field, value in fields.items():
        setattr(instance, field, value)

    update_fields = list(fields.keys())
    if hasattr(instance, 'updated_at'):
        update_fields.append('updated_at')

    instance.save(update_fields=update_fields)
