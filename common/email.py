"""Shared email-notification helper used by post_save signals."""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_notification(subject, template_base, context):
    """Send a notification email to settings.NOTIFICATION_EMAIL.

    Renders both `<template_base>.txt` and `<template_base>.html` from the template
    loader, builds a multipart message and dispatches it. Any exception during send
    is logged but never re-raised so a flaky SMTP host can never break the request
    that triggered the notification (e.g. a booking POST).
    """
    try:
        text_body = render_to_string(f'{template_base}.txt', context)
        html_body = render_to_string(f'{template_base}.html', context)
        message = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NOTIFICATION_EMAIL],
        )
        message.attach_alternative(html_body, 'text/html')
        message.send(fail_silently=False)
    except Exception:
        logger.exception(f'Failed to send notification email: {subject}')
