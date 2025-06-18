from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.db.models import Q

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    fullname = serializers.CharField(source='full_name', write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'fullname', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class CustomTokenObtainSerializer(serializers.Serializer):
    username_field = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username_field = attrs.get('username_field')
        password = attrs.get('password')

        if not username_field or not password:
            raise serializers.ValidationError(_('Must include "username_field" and "password".'))

        user = authenticate(username=username_field, password=password)
        
        if user is None:
            try:
                CustomUser.objects.get(
                    Q(username=username_field) | Q(email=username_field)
                )
                raise serializers.ValidationError(_('Invalid password.'))
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(_('No user found with this username or email.'))

        if not user.is_active:
            raise serializers.ValidationError(_('User account is disabled.'))

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name
            }
        }
