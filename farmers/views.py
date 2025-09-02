from crops.models import Crop
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.contrib.auth import get_user_model
from users.permissions import IsAdmin, IsFarmer
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class AdminDashboardView(APIView):
    '''
    Returns admin-specific dashboard data:
    - Total farmers
    - Total crops
    - Crops per farmer (for chart)
    '''
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_farmers = User.objects.filter(role=User.Role.FARMER).count()
        total_crops = Crop.objects.count()
 
        crops_per_farmer = (
            Crop.objects.values('farmer__id', 'farmer__username')
            .annotate(total_crops=Count('id'))
            .order_by('farmer__username')
        )

        return Response({
            'total_farmers': total_farmers,
            'total_crops': total_crops,
            'crops_per_farmer': list(crops_per_farmer),
        })


class FarmerDashboardView(APIView):
    '''
    Returns farmer-specific dashboard data:
    - Total crops owned by farmer
    - Crop counts by type (for chart)
    '''
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request):
        farmer = request.user

        total_crops = Crop.objects.filter(farmer=farmer).count()
 
        crops_by_type = (
            Crop.objects.filter(farmer=farmer)
            .values('crop_type')
            .annotate(count=Count('id'))
            .order_by('crop_type')
        )

        return Response({
            'total_crops': total_crops,
            'crops_by_type': list(crops_by_type),
        })