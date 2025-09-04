from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import FarmerDetailView, FarmerListCreateView, LogoutView, SignupView, CustomTokenObtainPairView, UserProfileView, UserProfileUpdateView

urlpatterns = [
    path('v1/signup/', SignupView.as_view(), name='signup_view'),
    path('v1/login/', CustomTokenObtainPairView.as_view(), name='login_view'),
    path('v1/logout/', LogoutView.as_view(), name='logout_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/profile/', UserProfileView.as_view(), name='user_profile_view'),
    path('v1/profile/update/', UserProfileUpdateView.as_view(), name='user_profile_update_view'),
    path('v1/farmers/', FarmerListCreateView.as_view(), name='farmer_list_create_view'),
    path('v1/farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmer_detail_view'),
]