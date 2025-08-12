#!/usr/bin/env python3
"""
Test script for user image upload functionality
"""
import requests
import json

# Test endpoints
BASE_URL = "http://localhost:8000"

def test_user_endpoints():
    """Test user-related endpoints"""
    
    # Test signup with fullname
    print("🔍 Testing user signup with fullname...")
    signup_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "fullname": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("✅ Signup successful!")
            user_data = response.json()
            print(f"User ID: {user_data['id']}")
            print(f"Email: {user_data['email']}")
            print(f"Fullname: {user_data.get('fullname', 'None')}")
            print(f"Image URL: {user_data.get('image_url', 'None')}")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test signin
    print("\n🔍 Testing user signin...")
    signin_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
        if response.status_code == 200:
            print("✅ Signin successful!")
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"Access token: {access_token[:50]}...")
            
            # Test profile endpoint
            print("\n🔍 Testing profile endpoint...")
            headers = {"Authorization": f"Bearer {access_token}"}
            profile_response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
            
            if profile_response.status_code == 200:
                print("✅ Profile endpoint working!")
                profile_data = profile_response.json()
                print(json.dumps(profile_data, indent=2))
            else:
                print(f"❌ Profile endpoint failed: {profile_response.status_code}")
                
        else:
            print(f"❌ Signin failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_user_endpoints()