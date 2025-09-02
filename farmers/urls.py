from django.urls import path
from .views import AdminDashboardView, FarmerDashboardView

urlpatterns = [ 
    # path('v1/farmers/', FarmerListView.as_view(), name='farmerListView'),
    # path('v1/farmers/<int:pk>/', FarmerDetailView.as_view(), name='farmerDetailView'), 
    path('v1/admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard_view'),
    path('v1/farmer/dashboard/', FarmerDashboardView.as_view(), name='farmer_dashboard_view'),
]