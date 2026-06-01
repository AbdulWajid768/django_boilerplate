"""Signal receivers for the site_content app (email notification on new contact form submissions)."""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.email import send_notification
from site_content.models import ContactMessage


@receiver(post_save, sender=ContactMessage, dispatch_uid='site_content_new_contact_email')
def notify_new_contact_message(sender, instance, created, **kwargs):
    """Email Maria whenever a new contact-form submission comes in."""
    if not created:
        return

    admin_url = f'{settings.BASE_URL}/admin/site_content/contactmessage/{instance.id}/change/'
    context = {
        'message': instance,
        'admin_url': admin_url,
    }
    send_notification(
        subject=f'New contact message from {instance.name}',
        template_base='emails/new_contact_message',
        context=context,
    )
