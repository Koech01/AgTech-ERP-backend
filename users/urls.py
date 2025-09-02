from django.urls import path
from .views import SignupView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/signup/', SignupView.as_view(), name='signup_view'),
    path('v1/login/', CustomTokenObtainPairView.as_view(), name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]