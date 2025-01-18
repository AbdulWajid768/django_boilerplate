"""Django admin configuration for user app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    """Handle User admin."""

    list_display = ['email', 'is_active', 'is_staff', 'is_superuser']
    add_fieldsets = [
        ('Create User', {
            'classes': ['wide'],
            'fields': ['email', 'password', 'confirm_password'],
        }),
    ]
    ordering = ['id']
    search_fields = ['first_name', 'last_name', 'email']


admin.site.register(User, UserAdmin)
