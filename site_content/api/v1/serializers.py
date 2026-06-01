"""Serializers for site_content v1 APIs."""
from rest_framework import serializers

from site_content.models import ContactMessage, PaymentInstruction, SiteSettings


class PaymentInstructionSerializer(serializers.ModelSerializer):
    """Public payment-instructions payload (singleton)."""

    class Meta:
        model = PaymentInstruction
        fields = [
            'id',
            'bank_name',
            'account_title',
            'account_number',
            'iban',
            'whatsapp_number',
            'payment_note',
        ]
        read_only_fields = fields


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Public site-settings payload (stats + about)."""

    profile_photo = serializers.ImageField(read_only=True)

    class Meta:
        model = SiteSettings
        fields = [
            'id',
            'clients_helped',
            'years_experience',
            'conditions_treated',
            'sessions_conducted',
            'about_text',
            'philosophy_quote',
            'profile_photo',
        ]
        read_only_fields = fields


class ContactMessageCreateSerializer(serializers.ModelSerializer):
    """Inbound serializer for the public contact form."""

    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'message']
        read_only_fields = ['id']
