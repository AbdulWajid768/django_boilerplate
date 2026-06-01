"""Signal receivers for the appointments app (email notifications on new bookings)."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from appointments.models import Appointment
from common.email import send_notification
from django.conf import settings


@receiver(post_save, sender=Appointment, dispatch_uid='appointments_new_booking_email')
def notify_new_appointment(sender, instance, created, **kwargs):
    """Email Maria whenever a new appointment is booked (created=True)."""
    if not created:
        return

    admin_url = f'{settings.BASE_URL}/admin/appointments/appointment/{instance.id}/change/'
    context = {
        'appointment': instance,
        'admin_url': admin_url,
        'wa_link': f'https://wa.me/{instance.client_phone.lstrip("+")}',
        'tel_link': f'tel:{instance.client_phone}',
    }
    send_notification(
        subject=f'New booking: {instance.client_name} - {instance.service.name}',
        template_base='emails/new_appointment',
        context=context,
    )
