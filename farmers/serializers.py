from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active']
        read_only_fields = ['id', 'role']  

    def update(self, instance, validated_data): 
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email).lower()
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance