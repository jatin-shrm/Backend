#!/usr/bin/env python3
"""
Test script for user profile and image upload functionality
Run this script to test the API endpoints
"""

import requests
import json
import os

# Configuration
BASE_URL = "http://127.0.0.1:8000"
AUTH_URL = f"{BASE_URL}/api/auth/token/"
PROFILE_URL = f"{BASE_URL}/api/users/profile/"
IMAGES_URL = f"{BASE_URL}/api/users/images/"

def test_authentication():
    """Test user authentication"""
    print("🔐 Testing Authentication...")
    
    # Test login
    login_data = {
        "username_field": "your_email@example.com",  # Replace with your email
        "password": "your_password"  # Replace with your password
    }
    
    response = requests.post(AUTH_URL, json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"Access Token: {data['access'][:50]}...")
        return data['access']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_profile_creation(access_token):
    """Test user profile creation/update"""
    print("\n👤 Testing Profile Creation...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    profile_data = {
        "height": 175.5,
        "gender": "M",
        "city": "Mumbai",
        "country": "India",
        "body_type": "athletic"
    }
    
    response = requests.post(PROFILE_URL, json=profile_data, headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile created/updated successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Profile creation failed: {response.status_code}")
        print(response.text)

def test_image_upload(access_token):
    """Test image upload"""
    print("\n📸 Testing Image Upload...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Create a simple test image (you can replace this with a real image file)
    test_image_path = "test_image.jpg"
    
    # Check if test image exists, if not create a placeholder
    if not os.path.exists(test_image_path):
        print("⚠️  No test image found. Please create a test_image.jpg file or update the path.")
        return
    
    with open(test_image_path, 'rb') as image_file:
        files = {
            'image': ('test_image.jpg', image_file, 'image/jpeg'),
        }
        data = {
            'is_profile': 'true'
        }
        
        response = requests.post(IMAGES_URL, files=files, data=data, headers=headers)
        
        if response.status_code == 201:
            print("✅ Image uploaded successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Image upload failed: {response.status_code}")
            print(response.text)

def test_get_profile(access_token):
    """Test getting user profile"""
    print("\n📋 Testing Get Profile...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(PROFILE_URL, headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile retrieved successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        print(response.text)

def test_get_images(access_token):
    """Test getting user images"""
    print("\n🖼️  Testing Get Images...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(IMAGES_URL, headers=headers)
    
    if response.status_code == 200:
        print("✅ Images retrieved successfully!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Images retrieval failed: {response.status_code}")
        print(response.text)

def main():
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Test authentication
    access_token = test_authentication()
    
    if not access_token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test profile functionality
    test_profile_creation(access_token)
    test_get_profile(access_token)
    
    # Test image functionality
    test_image_upload(access_token)
    test_get_images(access_token)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 