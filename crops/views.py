from .models import Crop
from django.db.models import Sum
from rest_framework import generics
from .serializers import CropSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from users.permissions import IsAdmin, IsFarmer 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

class FarmerCropStatsView(generics.GenericAPIView):
    """
    Provides statistics for the logged-in farmer:
    - Total quantity of crops (kgs)
    - Total crops count
    - Farmer's rank based on total crops quantity to other farmers
    Access: Farmers only
    """
    permission_classes = [IsAuthenticated, IsFarmer]

    def get(self, request, *args, **kwargs):
        stats = (
            Crop.objects.filter(farmer=request.user)
            .values('crop_type')
            .annotate(total_quantity=Sum('quantity'))
        )

        all_types = dict(Crop.CROP_TYPES)
        crop_data = []
        total_count = 0
        for key, label in all_types.items():
            matched = next((item for item in stats if item['crop_type'] == key), None)
            count = matched['total_quantity'] if matched else 0
            crop_data.append({'crop_type': label, 'count': count})
            total_count += count

        farmer_totals = (
            Crop.objects
            .values('farmer')
            .annotate(total_crops=Sum('quantity'))
            .order_by('-total_crops')
        )

        rank = 1
        for i, f in enumerate(farmer_totals, start=1):
            if f['farmer'] == request.user.id:
                rank = i
                break

        return Response({
            'crops_by_type': crop_data,
            'total_count': total_count,
            'rank': rank
        })
    

class AdminStatsView(generics.GenericAPIView):
    """
    Returns:
    - total farmers
    - total crops
    - crops per farmer for chart
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, *args, **kwargs): 
        total_farmers = User.objects.filter(role=User.Role.FARMER).count()
        total_crops = Crop.objects.aggregate(total=Sum('quantity'))['total'] or 0
 
        crops_per_farmer_qs = (
            Crop.objects.values('farmer__username')
            .annotate(total_crops=Sum('quantity'))
            .order_by('farmer__username')
        )
        crops_per_farmer = [
            {'farmer': item['farmer__username'], 'totalCrops': item['total_crops']}
            for item in crops_per_farmer_qs
        ]

        return Response({
            "username": request.user.username,
            "total_farmers": total_farmers,
            "total_crops": total_crops,
            "crops_per_farmer": crops_per_farmer
        })
    

class FarmerCropListCreateView(generics.ListCreateAPIView):
    """
    Provides admin-level statistics:
    - Total number of farmers
    - Total number of crops quantity
    - List of crops per farmer for chart
    Access: Admins only
    """
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:  
            return Crop.objects.all().order_by('-created')
        return Crop.objects.filter(farmer=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class FarmerCropRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete crops.
    - Farmers can only modify their own crops
    - Admin can delete any crop
    Access: Authenticated users
    """
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Crop.objects.filter(farmer=self.request.user)

    def perform_update(self, serializer):
        crop = self.get_object()
        if crop.farmer != self.request.user:
            raise PermissionDenied("You can only edit your own crops.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.farmer != self.request.user:
            raise PermissionDenied("You can only delete your own crops.")
        instance.delete()