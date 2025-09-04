from django.db import transaction  
from users.permissions import IsAdmin
from .serializers import UserSerializer
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# Custom token to include role
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # embed role in token
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(generics.CreateAPIView):
    '''
    Handles farmer signup. Admin accounts are created via management command.
    '''
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        refresh['username'] = user.username

        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveAPIView):
    """
    Returns current logged-in user's info including profile_icon URL.
    """
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data

        username = data.get('username', user.username)
        email = data.get('email', user.email)

        # Email validation
        if email != user.email:
            try:
                validate_email(email)
            except ValidationError:
                return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user.username = username
        user.email = email

        # Handle profile icon upload
        profile_icon = request.FILES.get('profileIcon')
        if profile_icon:
            user.profile_icon = profile_icon
        user.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'profile_icon': user.profile_icon.url if user.profile_icon else None
        }, status=status.HTTP_200_OK)
    

# List & Create Farmers (Admin only)
class FarmerListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role=User.Role.FARMER).order_by('-created')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        """
        Create a farmer via admin panel.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        farmer = serializer.save()

        if not farmer.profile_icon:
            farmer.profile_icon = 'profileIcon.png'
            farmer.save(update_fields=['profile_icon'])
        return Response(UserSerializer(farmer).data, status=status.HTTP_201_CREATED)


# Retrieve, Update, Delete Farmer (Admin only)
class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role=User.Role.FARMER)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
from rest_framework.renderers import JSONRenderer


class LogoutView(APIView):
    """
    Logout user by blacklisting the refresh token and clearing cookie.
    Only accepts POST requests.
    """
    permission_classes = [AllowAny] 
    renderer_classes = [JSONRenderer]
    http_method_names = ["post"]

    def post(self, request):
        refresh_token = request.COOKIES.get("refreshToken")  # only from cookie

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # token already invalid/blacklisted

        # Always clear the cookie, even if token invalid
        response = Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
        response.delete_cookie("refreshToken", path="/")
        return response