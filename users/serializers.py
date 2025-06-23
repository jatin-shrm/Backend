from rest_framework import serializers
from .models import UserProfile, UserImage
from authapp.models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'full_name', 'height', 'gender', 'city', 'country', 'body_type']
        read_only_fields = ['id', 'username', 'email', 'full_name']

class UserImageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserImage
        fields = ['id', 'username', 'image', 'is_profile', 'uploaded_at']
        read_only_fields = ['id', 'username', 'uploaded_at']

class UserImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['image', 'is_profile'] 

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name']
        read_only_fields = ['id', 'username', 'full_name'] 