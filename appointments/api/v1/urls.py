"""URLs for appointments v1 APIs."""
from django.urls import path

from appointments.api.v1 import views

urlpatterns = [
    path('appointments/', views.AppointmentCreateAPIView.as_view(), name='appointment_create_api'),
    path('appointments/mine/', views.MyAppointmentsListAPIView.as_view(), name='appointment_mine_list_api'),
    path(
        'appointments/mine/<uuid:booking_reference>/',
        views.MyAppointmentDetailAPIView.as_view(),
        name='appointment_mine_detail_api',
    ),
    path(
        'appointments/mine/<uuid:booking_reference>/cancel/',
        views.CancelMyAppointmentAPIView.as_view(),
        name='appointment_mine_cancel_api',
    ),
]
