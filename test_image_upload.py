#!/usr/bin/env python3
"""
Test script for image upload functionality
"""
import requests
import json
from PIL import Image
import io

BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image."""
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_image_upload():
    """Test the complete image upload flow."""
    
    # Step 1: Sign up a test user
    print("🔍 Step 1: Creating test user...")
    signup_data = {
        "email": "imagetest@example.com",
        "password": "testpass123",
        "fullname": "Image Test User"
    }
    
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if signup_response.status_code == 200:
            print("✅ User created successfully!")
            user_data = signup_response.json()
            print(f"User ID: {user_data['id']}")
        else:
            print(f"❌ Signup failed: {signup_response.status_code}")
            if signup_response.status_code == 400:
                print("User might already exist, continuing with signin...")
            else:
                print(signup_response.text)
                return
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return
    
    # Step 2: Sign in to get token
    print("\n🔍 Step 2: Signing in...")
    signin_data = {
        "email": "imagetest@example.com",
        "password": "testpass123"
    }
    
    try:
        signin_response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
        if signin_response.status_code == 200:
            print("✅ Signin successful!")
            token_data = signin_response.json()
            access_token = token_data['access_token']
            print(f"Token: {access_token[:50]}...")
        else:
            print(f"❌ Signin failed: {signin_response.status_code}")
            print(signin_response.text)
            return
    except Exception as e:
        print(f"❌ Signin error: {e}")
        return
    
    # Step 3: Upload image
    print("\n🔍 Step 3: Uploading test image...")
    test_image = create_test_image()
    
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
        
        upload_response = requests.post(f"{BASE_URL}/auth/upload-image", headers=headers, files=files)
        
        if upload_response.status_code == 200:
            print("✅ Image upload successful!")
            upload_data = upload_response.json()
            print(f"Image URL: {upload_data['image_url']}")
            print(f"Message: {upload_data['message']}")
        else:
            print(f"❌ Image upload failed: {upload_response.status_code}")
            print(upload_response.text)
            
    except Exception as e:
        print(f"❌ Upload error: {e}")

if __name__ == "__main__":
    test_image_upload()