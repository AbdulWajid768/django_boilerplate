"""Top-level API router for the v1 surface. Each app owns its own urls module."""
from django.urls import include, path

urlpatterns = [
    path('', include('accounts.api.v1.urls')),
    path('', include('services.api.v1.urls')),
    path('', include('slots.api.v1.urls')),
    path('', include('appointments.api.v1.urls')),
    path('', include('site_content.api.v1.urls')),
]
