"""URLs for services v1 APIs."""
from django.urls import path

from services.api.v1 import views

urlpatterns = [
    path('services/', views.ServiceListAPIView.as_view(), name='service_list_api'),
]
