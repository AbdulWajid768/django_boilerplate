"""URLs for site_content v1 APIs."""
from django.urls import path

from site_content.api.v1 import views

urlpatterns = [
    path('payment-instructions/', views.PaymentInstructionAPIView.as_view(), name='payment_instructions_api'),
    path('site-settings/', views.SiteSettingsAPIView.as_view(), name='site_settings_api'),
    path('contact/', views.ContactMessageCreateAPIView.as_view(), name='contact_create_api'),
]
