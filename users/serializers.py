from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_icon = serializers.ImageField(max_length=None, use_url=True, required=False) 

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'profile_icon', 'created')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'profile_icon', 'created')

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.FARMER,
            profile_icon=validated_data.get('profile_icon')
        )