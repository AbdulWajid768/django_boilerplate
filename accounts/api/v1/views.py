"""V1 APIs for accounts app."""
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.v1.serializers import SignupSerializer
from accounts.api.v1.validators import LoginValidator
from accounts.util import create_auth_data
from common.utils import apply_validation


class SignupAPIView(APIView):
    def post(self, request):
        serializer = apply_validation(SignupSerializer, request.data)
        user = serializer.save()
        return Response(data=create_auth_data(user), status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        validator = apply_validation(LoginValidator, request.data)
        credentials = validator.validated_data

        if not (user := authenticate(email=credentials['email'], password=credentials['password'])):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(data=create_auth_data(user), status=status.HTTP_200_OK)


class GoogleLoginAPIView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_CALLBACK_URL
    client_class = OAuth2Client
