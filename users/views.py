from django.db import transaction  
from users.permissions import IsAdmin
from .serializers import UserSerializer
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the default JWT token serializer to include the user's role in the token payload.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  
        return token

    def validate(self, attrs): 
        data = super().validate(attrs)
        data['role'] = self.user.role  
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignupView(generics.CreateAPIView):
    """ 
    Admin accounts are created separately via management command.
    Returns user info and JWT tokens on success.
    """
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
    Retrieves current logged-in user's information. 
    Access: Authenticated users
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(APIView):
    """
    Allows authenticated users to update their profile:
    - username, email, and profile icon
    - validates email uniqueness and format
    Access: both admin and farmer
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data

        username = data.get('username', user.username)
        email = data.get('email', user.email)
 
        if email != user.email:
            try:
                validate_email(email)
            except ValidationError:
                return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user.username = username
        user.email = email
 
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
    

class FarmerListCreateView(generics.ListCreateAPIView):
    """
    List all farmers or create a new farmer (Admin only). 
    """
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


class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific farmer (Admin only).
    """
    queryset = User.objects.filter(role=User.Role.FARMER)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class LogoutView(APIView):
    """
    Logs out a user by:
    - Blacklisting the refresh token (if present)
    - Clearing the refresh token cookie
    Access: Public (anyone can call)
    Method: POST only
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