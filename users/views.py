from django.db import transaction  
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

# Custom token to include role
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Handles farmer signup. Admin accounts are created via management command.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        refresh["username"] = user.username

        self.response_payload = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
        }

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_payload, status=status.HTTP_201_CREATED)