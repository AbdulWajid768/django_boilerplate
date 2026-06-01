"""Admin configuration for the slots app."""
from django.contrib import admin, messages

from slots.models import AvailableSlot


@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    """Admin surface for weekly AvailableSlot patterns with soft-delete."""

    list_display = [
        'weekday_label',
        'start_time',
        'end_time',
        'slot_type',
        'is_disabled',
        'is_deleted',
    ]
    list_editable = ['is_disabled']
    list_filter = ['weekday', 'slot_type', 'is_disabled', 'is_deleted']
    search_fields = ['notes']
    ordering = ['weekday', 'start_time']
    actions = ['enable_slots', 'disable_slots', 'soft_delete_slots', 'restore_slots']

    def get_queryset(self, request):
        """Include soft-deleted rows so admin can restore them."""
        return AvailableSlot.all_objects.all()

    def delete_model(self, request, obj):
        """Soft-delete instead of removing the row."""
        obj.is_deleted = True
        obj.save(update_fields=['is_deleted', 'updated_at'])

    def delete_queryset(self, request, queryset):
        """Soft-delete bulk selections."""
        queryset.update(is_deleted=True)

    @admin.action(description='Enable selected slots')
    def enable_slots(self, request, queryset):
        """Bulk-enable selected slots."""
        updated = queryset.update(is_disabled=False)
        self.message_user(request, f'{updated} slot(s) enabled.', messages.SUCCESS)

    @admin.action(description='Disable selected slots')
    def disable_slots(self, request, queryset):
        """Bulk-disable selected slots."""
        updated = queryset.update(is_disabled=True)
        self.message_user(request, f'{updated} slot(s) disabled.', messages.SUCCESS)

    @admin.action(description='Soft-delete selected slots')
    def soft_delete_slots(self, request, queryset):
        """Mark selected slots as deleted without removing historical appointments."""
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f'{updated} slot(s) soft-deleted.', messages.SUCCESS)

    @admin.action(description='Restore selected slots')
    def restore_slots(self, request, queryset):
        """Restore soft-deleted slots back to the booking calendar."""
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f'{updated} slot(s) restored.', messages.SUCCESS)

    @admin.display(description='Weekday', ordering='weekday')
    def weekday_label(self, obj):
        """Human-readable weekday label."""
        return obj.get_weekday_display()
