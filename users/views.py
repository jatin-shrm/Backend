from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import UserProfile, UserImage
from .serializers import UserProfileSerializer, UserImageSerializer, UserImageUploadSerializer, UserListSerializer
from authapp.models import CustomUser

# Create your views here.

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        """Create or update user profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        except UserProfile.DoesNotExist:
            serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        """Get all images for the user"""
        images = UserImage.objects.filter(user=request.user)
        serializer = UserImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Upload a new image"""
        serializer = UserImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            # If this is a profile image, unset other profile images
            if serializer.validated_data.get('is_profile', False):
                UserImage.objects.filter(user=request.user, is_profile=True).update(is_profile=False)
            
            image = serializer.save(user=request.user)
            response_serializer = UserImageSerializer(image)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserImageDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, image_id):
        """Delete a specific image"""
        try:
            image = UserImage.objects.get(id=image_id, user=request.user)
            image.delete()
            return Response({'message': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UserImage.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, image_id):
        """Update image (e.g., set as profile image)"""
        try:
            image = UserImage.objects.get(id=image_id, user=request.user)
            serializer = UserImageUploadSerializer(image, data=request.data, partial=True)
            
            if serializer.is_valid():
                # If setting as profile image, unset other profile images
                if serializer.validated_data.get('is_profile', False):
                    UserImage.objects.filter(user=request.user, is_profile=True).exclude(id=image_id).update(is_profile=False)
                
                serializer.save()
                response_serializer = UserImageSerializer(image)
                return Response(response_serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserImage.DoesNotExist:
            return Response({'message': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all users for chat with filtering (excluding current user)"""
        # Get query parameters
        gender = request.query_params.get('gender', None)
        city = request.query_params.get('city', None)
        body_type = request.query_params.get('body_type', None)
        search = request.query_params.get('search', None)
        
        # Start with all users except current user
        users = CustomUser.objects.exclude(id=request.user.id)
        
        # Apply filters
        if gender:
            # Filter by gender through UserProfile
            users = users.filter(profile__gender=gender)
        
        if city:
            # Filter by city through UserProfile
            users = users.filter(profile__city__icontains=city)
        
        if body_type:
            # Filter by body type through UserProfile
            users = users.filter(profile__body_type=body_type)
        
        if search:
            # Search in username and full_name
            users = users.filter(
                Q(username__icontains=search) | 
                Q(full_name__icontains=search)
            )
        
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)