"""Django admin configuration for the accounts app."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import Client, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for the email-based custom User model."""

    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    ordering = ['email']
    search_fields = ['email', 'first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin for the Client profile attached to each User."""

    list_display = ['user', 'phone', 'profile_complete', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['profile_complete', 'created_at']
    readonly_fields = ['user', 'google_id', 'created_at', 'updated_at']
    fields = ['user', 'phone', 'google_id', 'profile_complete', 'created_at', 'updated_at']
