from rest_framework import generics, status
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction 
from rest_framework_simplejwt.tokens import RefreshToken


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
    Handles farmer signup.
    Admin accounts should be created via management command.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        Custom POST handler to:
        - Validate incoming data
        - Create user as farmer by default
        - Return JWT tokens on success
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user instance
        user = serializer.save(role=User.Role.FARMER)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        refresh['username'] = user.username

        # Prepare response payload
        data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)