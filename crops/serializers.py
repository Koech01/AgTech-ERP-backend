from .models import Crop
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CropSerializer(serializers.ModelSerializer):
    farmer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.Role.FARMER), source='farmer', write_only=True, required=False)
    farmer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Crop
        fields = ['id', 'farmer', 'farmer_id', 'name', 'crop_type', 'quantity', 'created']


class CropCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['name', 'crop_type', 'quantity']