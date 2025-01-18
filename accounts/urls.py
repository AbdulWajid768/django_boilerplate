"""URLs for accounts views and apis."""

from django.urls import include, path

urlpatterns = [
    path('api/', include('accounts.api.urls')),
]
