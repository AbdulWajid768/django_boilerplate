"""Admin configuration for the services app."""
from django.contrib import admin

from services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin surface for the Service catalog."""

    list_display = [
        'name',
        'duration_minutes',
        'fee_online',
        'fee_inperson',
        'available_online',
        'available_inperson',
        'display_order',
        'is_active',
    ]
    list_editable = ['display_order', 'is_active']
    list_filter = ['is_active', 'available_online', 'available_inperson']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
