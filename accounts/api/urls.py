"""URLs for accounts apis."""

from django.urls import include, path

urlpatterns = [
    path('v1/accounts/', include('accounts.api.v1.urls')),
]
