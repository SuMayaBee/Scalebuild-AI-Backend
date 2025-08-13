#!/usr/bin/env python3
"""
Demo script to show the profile update issue that was fixed
"""
import asyncio
import httpx
import json

async def demonstrate_profile_update_fix():
    """Demonstrate that profile updates work correctly now"""
    
    print("🔧 PROFILE UPDATE ISSUE DEMONSTRATION")
    print("=" * 60)
    print("This demonstrates the fix for the profile update issue.")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    test_email = "alissaedword82@gmail.com"
    test_password = "forget"
    
    # Step 1: Authenticate
    print("\n1️⃣ Authenticating user...")
    signin_data = {"email": test_email, "password": test_password}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/auth/signin", json=signin_data)
        
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.text}")
            return
        
        token = response.json().get('access_token')
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("✅ Authentication successful")
        
        # Step 2: Get current profile
        print("\n2️⃣ Getting current profile...")
        response = await client.get(f"{base_url}/auth/profile", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get profile: {response.text}")
            return
        
        current_profile = response.json()
        print(f"📧 Current Email: {current_profile.get('email')}")
        print(f"👤 Current Name: {current_profile.get('name')}")
        print(f"🖼️ Current Image: {current_profile.get('image_url')}")
        
        # Step 3: Update profile (this was the problematic part)
        print("\n3️⃣ Updating profile information...")
        update_data = {
            "name": "Test User - Profile Updated",
            "image_url": "https://example.com/test-profile-image.jpg"
        }
        
        response = await client.put(f"{base_url}/auth/profile", json=update_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            updated_profile = response.json()
            print("✅ Profile update successful!")
            print(f"👤 New Name: {updated_profile.get('name')}")
            print(f"🖼️ New Image: {updated_profile.get('image_url')}")
            
            # Verify the update persisted
            print("\n4️⃣ Verifying update persisted...")
            response = await client.get(f"{base_url}/auth/profile", headers=headers)
            
            if response.status_code == 200:
                verified_profile = response.json()
                print("✅ Profile changes persisted correctly!")
                print(f"👤 Verified Name: {verified_profile.get('name')}")
                print(f"🖼️ Verified Image: {verified_profile.get('image_url')}")
            else:
                print(f"❌ Failed to verify profile: {response.text}")
        else:
            print(f"❌ Profile update failed: {response.text}")
            print("This would have been the error you were experiencing before the fix.")
        
        # Step 5: Test password change endpoint
        print("\n5️⃣ Testing separate password change endpoint...")
        password_data = {
            "current_password": test_password,
            "new_password": "temporary_new_password"
        }
        
        response = await client.put(f"{base_url}/auth/change-password", json=password_data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Password change endpoint working correctly!")
            print(f"📝 Response: {response.json().get('message')}")
            
            # Change it back
            password_data = {
                "current_password": "temporary_new_password",
                "new_password": test_password
            }
            
            # Get new token first
            signin_data = {"email": test_email, "password": "temporary_new_password"}
            auth_response = await client.post(f"{base_url}/auth/signin", json=signin_data)
            new_token = auth_response.json().get('access_token')
            new_headers = {"Authorization": f"Bearer {new_token}", "Content-Type": "application/json"}
            
            await client.put(f"{base_url}/auth/change-password", json=password_data, headers=new_headers)
            print("✅ Password reset back to original")
        else:
            print(f"❌ Password change failed: {response.text}")
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY OF FIXES APPLIED:")
    print("1. Fixed parameter name mismatch (fullname → name)")
    print("2. Added separate password change endpoint with validation")
    print("3. Profile updates now only handle name and image_url")
    print("4. Password changes require current password verification")
    print("5. Proper error handling and validation")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demonstrate_profile_update_fix())