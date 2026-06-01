"""URLs for accounts v1 APIs (Google id_token sign-in + JWT refresh + client profile)."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.v1 import views

urlpatterns = [
    path('auth/google/', views.GoogleLoginAPIView.as_view(), name='google_login_api'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('clients/me/', views.ClientMeAPIView.as_view(), name='client_me_api'),
]
