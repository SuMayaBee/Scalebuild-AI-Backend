#!/usr/bin/env python3
"""
Complete user image upload example
"""
import requests
import json
from PIL import Image
import io
import os

BASE_URL = "http://localhost:8000"

def create_test_user_and_upload():
    """Complete flow: signup, signin, upload image"""
    
    # Step 1: Create a user (or use existing)
    print("🔍 Step 1: Creating/using test user...")
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "fullname": "Test User"
    }
    
    # Try to sign up (might fail if user exists)
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if signup_response.status_code == 200:
            print("✅ New user created!")
        else:
            print("ℹ️ User might already exist, continuing...")
    except Exception as e:
        print(f"Signup error: {e}")
    
    # Step 2: Sign in to get token
    print("\n🔍 Step 2: Getting authentication token...")
    signin_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    try:
        signin_response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
        if signin_response.status_code == 200:
            token_data = signin_response.json()
            access_token = token_data['access_token']
            print(f"✅ Token obtained: {access_token[:30]}...")
        else:
            print(f"❌ Signin failed: {signin_response.status_code}")
            print(signin_response.text)
            return
    except Exception as e:
        print(f"❌ Signin error: {e}")
        return
    
    # Step 3: Create a test image (or use existing file)
    print("\n🔍 Step 3: Preparing image...")
    
    # Option A: Create a simple test image
    def create_test_image():
        img = Image.new('RGB', (200, 200), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return img_bytes
    
    # Option B: Use existing image file (uncomment if you have one)
    # image_path = "/path/to/your/image.jpg"
    # if os.path.exists(image_path):
    #     with open(image_path, 'rb') as f:
    #         image_data = f.read()
    #     image_file = io.BytesIO(image_data)
    # else:
    #     image_file = create_test_image()
    
    image_file = create_test_image()
    print("✅ Test image created")
    
    # Step 4: Upload the image
    print("\n🔍 Step 4: Uploading image...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        files = {"file": ("profile_image.jpg", image_file, "image/jpeg")}
        
        upload_response = requests.post(f"{BASE_URL}/auth/upload-image", headers=headers, files=files)
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            print("🎉 Image upload successful!")
            print(f"📸 Image URL: {upload_data['image_url']}")
            print(f"💬 Message: {upload_data['message']}")
            
            # Show updated user data
            user_data = upload_data['user']
            print(f"\n👤 Updated User Info:")
            print(f"   ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Full Name: {user_data['fullname']}")
            print(f"   Image URL: {user_data['image_url']}")
            
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            print(upload_response.text)
            
    except Exception as e:
        print(f"❌ Upload error: {e}")

def get_user_profile(email, password):
    """Get user profile to see current image"""
    print(f"\n🔍 Getting profile for {email}...")
    
    # Sign in
    signin_data = {"email": email, "password": password}
    signin_response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
    
    if signin_response.status_code == 200:
        token = signin_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get profile
        profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        
        if profile_response.status_code == 200:
            profile = profile_response.json()
            print("👤 Current Profile:")
            print(json.dumps(profile, indent=2))
        else:
            print(f"❌ Profile fetch failed: {profile_response.status_code}")
    else:
        print(f"❌ Signin failed: {signin_response.status_code}")

if __name__ == "__main__":
    print("🚀 User Image Upload Demo")
    print("=" * 50)
    
    # Upload image
    create_test_user_and_upload()
    
    # Check profile
    get_user_profile("testuser@example.com", "testpass123")