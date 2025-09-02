from .models import Crop
from rest_framework import generics
from .serializers import CropSerializer
from users.permissions import IsAdmin, IsFarmer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class CropListViewAdmin(generics.ListAPIView):
    queryset = Crop.objects.all().select_related('farmer')
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class CropDetailViewAdmin(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crop.objects.all().select_related('farmer')
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class CropListViewFarmer(generics.ListCreateAPIView):
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsFarmer]

    def get_queryset(self):
        return Crop.objects.filter(farmer=self.request.user).select_related('farmer')

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class CropDetailViewFarmer(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsFarmer]

    def get_queryset(self):
        return Crop.objects.filter(farmer=self.request.user)