from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/signup/', RegisterView.as_view(), name='registerView'),
    path('v1/register/', CustomTokenObtainPairView.as_view(), name='loginView'),
    path('token/refresh/', TokenRefreshView.as_view(), name='tokenRefresh'),
]