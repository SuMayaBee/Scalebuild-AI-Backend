#!/usr/bin/env python3
"""
Script to demonstrate the correct way to test change-password endpoint
"""
import asyncio
import httpx
import json

async def test_change_password_with_auth():
    """Test change password with proper authentication"""
    
    base_url = "http://localhost:8000"
    test_email = "alissaedword82@gmail.com"
    current_password = "forget"
    new_password = "newpassword123"
    
    print("🔐 Testing Change Password with Proper Authentication")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Step 1: Sign in to get token
        print("1️⃣ Signing in to get authentication token...")
        signin_data = {
            "email": test_email,
            "password": current_password
        }
        
        response = await client.post(f"{base_url}/auth/signin", json=signin_data)
        
        if response.status_code != 200:
            print(f"❌ Signin failed: {response.text}")
            return
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        print(f"✅ Got access token: {access_token[:50]}...")
        
        # Step 2: Use token to change password
        print("\n2️⃣ Using token to change password...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        password_data = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        response = await client.put(
            f"{base_url}/auth/change-password", 
            json=password_data, 
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Password changed successfully: {result.get('message')}")
            
            # Step 3: Test new password works
            print("\n3️⃣ Testing signin with new password...")
            new_signin_data = {
                "email": test_email,
                "password": new_password
            }
            
            response = await client.post(f"{base_url}/auth/signin", json=new_signin_data)
            
            if response.status_code == 200:
                print("✅ New password works!")
                
                # Step 4: Change password back
                print("\n4️⃣ Changing password back to original...")
                new_token = response.json().get("access_token")
                new_headers = {
                    "Authorization": f"Bearer {new_token}",
                    "Content-Type": "application/json"
                }
                
                reset_data = {
                    "current_password": new_password,
                    "new_password": current_password
                }
                
                response = await client.put(
                    f"{base_url}/auth/change-password", 
                    json=reset_data, 
                    headers=new_headers
                )
                
                if response.status_code == 200:
                    print("✅ Password reset back to original")
                else:
                    print(f"❌ Failed to reset password: {response.text}")
            else:
                print(f"❌ New password doesn't work: {response.text}")
        else:
            print(f"❌ Password change failed: {response.text}")
            if response.status_code == 403:
                print("💡 This is likely due to missing or invalid authentication token")
    
    print("\n" + "=" * 60)
    print("📋 CURL COMMAND EXAMPLES:")
    print("\n1. Get authentication token:")
    print('curl -X POST "http://localhost:8000/auth/signin" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email": "alissaedword82@gmail.com", "password": "forget"}\'')
    
    print("\n2. Change password (replace YOUR_TOKEN with actual token):")
    print('curl -X PUT "http://localhost:8000/auth/change-password" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -H "Authorization: Bearer YOUR_TOKEN" \\')
    print('  -d \'{"current_password": "forget", "new_password": "newpass"}\'')
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_change_password_with_auth())