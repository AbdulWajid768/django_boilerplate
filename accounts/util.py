from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserSerializer


def create_auth_data(user):
    """Return auth data based on user."""
    user_serializer = UserSerializer(user)
    user_data = user_serializer.data
    tokens = RefreshToken.for_user(user)
    return {
        'tokens': {
            'access': str(tokens.access_token),
            'refresh': str(tokens)
        },
        'user': user_data
    }
