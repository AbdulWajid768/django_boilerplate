"""URLs for accounts v1 apis."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.v1 import views

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup_api'),
    path('login/', views.LoginAPIView.as_view(), name='login_api'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh_api'),
    path('login/google/', views.GoogleLoginAPIView.as_view(), name='google_login_api'),
]
