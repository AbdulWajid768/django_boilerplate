"""URLs for accounts v1 apis."""
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.urls import path, include

from accounts.api.v1 import views


urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup_api'),
    path('login/', views.LoginAPIView.as_view(), name='login_api'),
    path('login/google/', views.GoogleLoginAPIView.as_view(), name='google_login_api'),
]
