"""Admin configuration for the appointments app."""
from urllib.parse import quote

from django.contrib import admin, messages
from django.utils.html import format_html

from appointments.models import Appointment, AppointmentStatus


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin surface for Appointment with WhatsApp quick-link and bulk status actions."""

    list_display = [
        'short_reference',
        'client_name',
        'client_phone',
        'service',
        'appointment_date',
        'appointment_time',
        'appointment_type',
        'status',
        'whatsapp_link',
        'created_at',
    ]
    list_filter = ['status', 'appointment_type', 'service', 'appointment_date']
    search_fields = ['client_name', 'client_email', 'client_phone', 'booking_reference']
    date_hierarchy = 'appointment_date'
    ordering = ['-appointment_date', '-created_at']
    actions = ['mark_as_confirmed', 'mark_as_declined']

    readonly_fields = [
        'booking_reference',
        'client_user',
        'client_name',
        'client_email',
        'client_phone',
        'service',
        'slot',
        'appointment_type',
        'client_notes',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('Booking', {
            'fields': (
                'booking_reference',
                'service',
                'slot',
                'appointment_date',
                'appointment_type',
                'status',
            ),
        }),
        ('Client', {
            'fields': (
                'client_user',
                'client_name',
                'client_email',
                'client_phone',
                'client_notes',
            ),
        }),
        ('Admin', {
            'fields': (
                'admin_notes',
                'cancelled_by',
                'cancellation_reason',
                'created_at',
                'updated_at',
            ),
        }),
    )

    @admin.display(description='Ref', ordering='booking_reference')
    def short_reference(self, obj):
        """Show the first 8 chars of the booking_reference for compact lists."""
        return f'{str(obj.booking_reference)[:8]}'

    @admin.display(description='Time', ordering='slot__start_time')
    def appointment_time(self, obj):
        """Surface slot start time in the list view."""
        return obj.slot.start_time.strftime('%I:%M %p').lstrip('0') if obj.slot_id else '—'

    @admin.display(description='WhatsApp')
    def whatsapp_link(self, obj):
        """Render a clickable WhatsApp deep link pre-filled with the booking reference."""
        phone = (obj.client_phone or '').replace(' ', '').replace('-', '').lstrip('+')
        if not phone:
            return '—'
        text = f"Hi {obj.client_name}, regarding your appointment {str(obj.booking_reference)[:8]}"
        href = f'https://wa.me/{phone}?text={quote(text)}'
        return format_html('<a href="{}" target="_blank" rel="noopener">Open WhatsApp</a>', href)

    @admin.action(description='Mark selected appointments as Confirmed')
    def mark_as_confirmed(self, request, queryset):
        """Bulk-confirm selected appointments."""
        updated = 0
        for appointment in queryset:
            if appointment.status != AppointmentStatus.CONFIRMED:
                appointment.status = AppointmentStatus.CONFIRMED
                appointment.save()
                updated += 1
        self.message_user(request, f'{updated} appointment(s) confirmed.', messages.SUCCESS)

    @admin.action(description='Mark selected appointments as Declined')
    def mark_as_declined(self, request, queryset):
        """Bulk-decline selected appointments."""
        updated = 0
        for appointment in queryset:
            if appointment.status != AppointmentStatus.DECLINED:
                appointment.status = AppointmentStatus.DECLINED
                appointment.save()
                updated += 1
        self.message_user(request, f'{updated} appointment(s) declined.', messages.SUCCESS)
