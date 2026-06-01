"""Accounts v1 API views: Google id_token sign-in and client profile management."""
from django.conf import settings
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.v1.serializers import ClientProfileSerializer
from accounts.api.v1.validators import GoogleLoginValidator
from accounts.models import Client, User
from accounts.util import create_auth_data
from common.utils import apply_validation


class GoogleLoginAPIView(APIView):
    """Verify a Google id_token, upsert User+Client, return Django JWTs."""

    def post(self, request):
        """Validate the Google id_token and return JWT access/refresh + user payload."""
        validator = apply_validation(GoogleLoginValidator, request.data)
        token = validator.validated_data['id_token']

        try:
            claims = google_id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID or None,
            )
        except ValueError as exc:
            return Response(
                {'error': f'Invalid Google id_token: {exc}'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = claims.get('email')
        if not email or not claims.get('email_verified', False):
            return Response(
                {'error': 'Google account email is missing or not verified.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': claims.get('given_name', '') or '',
                'last_name': claims.get('family_name', '') or '',
                'is_active': True,
            },
        )

        Client.objects.get_or_create(
            user=user,
            defaults={'google_id': claims.get('sub', '') or ''},
        )

        return Response(data=create_auth_data(user), status=status.HTTP_200_OK)


class ClientMeAPIView(APIView):
    """GET or PATCH the logged-in client's profile (phone only is editable)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the current user's Client profile."""
        client, _ = Client.objects.get_or_create(user=request.user)
        return Response(ClientProfileSerializer(client).data)

    def patch(self, request):
        """Patch the editable Client fields (phone)."""
        client, _ = Client.objects.get_or_create(user=request.user)
        serializer = ClientProfileSerializer(client, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
