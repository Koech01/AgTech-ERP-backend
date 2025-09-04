from django.urls import path
from .views import FarmerCropListCreateView, FarmerCropRetrieveUpdateDestroyView, FarmerCropStatsView, AdminStatsView 

urlpatterns = [
    # Admin routes
    path('v1/crops/stats/', AdminStatsView.as_view(), name='admin_crop_stats_view'),
    # Farmer routes
    path('v1/farmer/crops/stats/', FarmerCropStatsView.as_view(), name='farmer_crop_stats_view'),
    path('v1/farmer/crops/', FarmerCropListCreateView.as_view(), name='farmer_crop_list_create_view'),
    path('v1/farmer/crops/<int:pk>/', FarmerCropRetrieveUpdateDestroyView.as_view(), name='farmer_crop_detail_view'),
]