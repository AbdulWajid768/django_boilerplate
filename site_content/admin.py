"""Admin configuration for the site_content app."""
from django.contrib import admin, messages
from django.utils.html import format_html

from site_content.models import ContactMessage, PaymentInstruction, SiteSettings


class SingletonAdmin(admin.ModelAdmin):
    """Base ModelAdmin enforcing at-most-one row for singleton models."""

    def has_add_permission(self, request):
        """Disallow adding a second row once one exists."""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Disallow deleting the lone singleton row."""
        return False


@admin.register(PaymentInstruction)
class PaymentInstructionAdmin(SingletonAdmin):
    """Singleton admin for bank-transfer payment instructions."""

    list_display = ['bank_name', 'account_title', 'account_number', 'whatsapp_number']
    fields = ['bank_name', 'account_title', 'account_number', 'iban', 'whatsapp_number', 'payment_note']

    def changelist_view(self, request, extra_context=None):
        """Warn admin when the singleton hasn't been created yet."""
        if not self.model.objects.exists():
            self.message_user(
                request,
                'No PaymentInstruction exists yet. Click "Add Payment instruction" to create it.',
                messages.WARNING,
            )
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    """Singleton admin for site-wide stats and About copy."""

    list_display = [
        'clients_helped',
        'years_experience',
        'conditions_treated',
        'sessions_conducted',
    ]
    readonly_fields = ['profile_photo_preview']
    fields = [
        'clients_helped',
        'years_experience',
        'conditions_treated',
        'sessions_conducted',
        'about_text',
        'philosophy_quote',
        'profile_photo',
        'profile_photo_preview',
    ]

    @admin.display(description='Profile photo preview')
    def profile_photo_preview(self, obj):
        """Show a small preview of the uploaded profile photo, if any."""
        if obj and obj.profile_photo:
            return format_html(
                '<img src="{}" style="max-height: 220px; border-radius: 8px;" />',
                obj.profile_photo.url,
            )
        return 'No photo uploaded yet.'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin surface for contact-form submissions."""

    list_display = ['name', 'email', 'phone', 'short_message', 'created_at', 'is_read']
    list_editable = ['is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']
    actions = ['mark_as_read']

    @admin.display(description='Message')
    def short_message(self, obj):
        """Truncate the message for the list view."""
        if not obj.message:
            return ''
        return f'{obj.message[:60]}...' if len(obj.message) > 60 else obj.message

    @admin.action(description='Mark selected messages as read')
    def mark_as_read(self, request, queryset):
        """Bulk-mark messages as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.', messages.SUCCESS)
