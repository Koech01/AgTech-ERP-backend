from django.urls import path
from .views import CropListViewAdmin, CropDetailViewAdmin, CropListViewFarmer,  CropDetailViewFarmer   


urlpatterns = [
    # Admin routes
    path('v1/crops/', CropListViewAdmin.as_view(), name='crop_list_admin_view'),
    path('v1/crops/<int:pk>/', CropDetailViewAdmin.as_view(), name='crop_detail_admin_view'),

    # Farmer routes
    path('v1/farmer/crops/', CropListViewFarmer.as_view(), name='crop_list_farmer_view'),
    path('v1/farmer/crops/<int:pk>/', CropDetailViewFarmer.as_view(), name='crop_detail_farmer_view'),
]
