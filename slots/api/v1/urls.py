"""URLs for slots v1 APIs."""
from django.urls import path

from slots.api.v1 import views

urlpatterns = [
    path('slots/', views.AvailableSlotListAPIView.as_view(), name='slot_list_api'),
    path('slots/available-dates/', views.AvailableDatesAPIView.as_view(), name='slot_available_dates_api'),
]
