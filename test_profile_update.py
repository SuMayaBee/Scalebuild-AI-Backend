#!/usr/bin/env python3
"""
Test script to verify profile update and password change functionality
"""
import asyncio
import httpx
import json
from typing import Dict, Any

class ProfileUpdateTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_email = "alissaedword82@gmail.com"
        self.test_password = "forget"
        self.new_password = "newpassword123"
        self.access_token = None
    
    async def authenticate(self) -> bool:
        """Authenticate and get access token"""
        print(f"🔐 Authenticating {self.test_email}...")
        
        signin_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/signin",
                    json=signin_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data.get('access_token')
                    print(f"✅ Authentication successful")
                    return True
                else:
                    print(f"❌ Authentication failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Authentication error: {str(e)}")
                return False
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def test_profile_update(self) -> bool:
        """Test updating profile information"""
        print(f"\n👤 Testing Profile Update...")
        
        update_data = {
            "name": "Alissa Edward Updated",
            "image_url": "https://example.com/new-profile-image.jpg"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(
                    f"{self.base_url}/auth/profile",
                    json=update_data,
                    headers=self.get_headers(),
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    profile_data = response.json()
                    print(f"✅ Profile update successful!")
                    print(f"👤 Updated Name: {profile_data.get('name')}")
                    print(f"🖼️ Updated Image URL: {profile_data.get('image_url')}")
                    return True
                else:
                    print(f"❌ Profile update failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Profile update error: {str(e)}")
                return False
    
    async def test_password_change_wrong_current(self) -> bool:
        """Test password change with wrong current password"""
        print(f"\n🔐 Testing Password Change (Wrong Current Password)...")
        
        password_data = {
            "current_password": "wrongpassword",
            "new_password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(
                    f"{self.base_url}/auth/change-password",
                    json=password_data,
                    headers=self.get_headers(),
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 400:
                    error_detail = response.json().get('detail')
                    print(f"✅ Correctly rejected wrong password: {error_detail}")
                    return True
                else:
                    print(f"❌ Should have rejected wrong password: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Password change error: {str(e)}")
                return False
    
    async def test_password_change_correct(self) -> bool:
        """Test password change with correct current password"""
        print(f"\n🔐 Testing Password Change (Correct Current Password)...")
        
        password_data = {
            "current_password": self.test_password,
            "new_password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(
                    f"{self.base_url}/auth/change-password",
                    json=password_data,
                    headers=self.get_headers(),
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Password change successful: {result.get('message')}")
                    return True
                else:
                    print(f"❌ Password change failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Password change error: {str(e)}")
                return False
    
    async def test_signin_with_new_password(self) -> bool:
        """Test signin with the new password"""
        print(f"\n🔐 Testing Signin with New Password...")
        
        signin_data = {
            "email": self.test_email,
            "password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/signin",
                    json=signin_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    token_data = response.json()
                    print(f"✅ Signin with new password successful!")
                    print(f"🔑 New Token: {token_data.get('access_token', '')[:50]}...")
                    return True
                else:
                    print(f"❌ Signin with new password failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Signin error: {str(e)}")
                return False
    
    async def test_signin_with_old_password(self) -> bool:
        """Test that old password no longer works"""
        print(f"\n🔐 Testing Signin with Old Password (Should Fail)...")
        
        signin_data = {
            "email": self.test_email,
            "password": self.test_password  # Old password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/signin",
                    json=signin_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 400:
                    error_detail = response.json().get('detail')
                    print(f"✅ Correctly rejected old password: {error_detail}")
                    return True
                else:
                    print(f"❌ Should have rejected old password: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Signin error: {str(e)}")
                return False
    
    async def reset_password_back(self) -> bool:
        """Reset password back to original for future tests"""
        print(f"\n🔄 Resetting Password Back to Original...")
        
        # First authenticate with new password
        signin_data = {
            "email": self.test_email,
            "password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # Get new token
                response = await client.post(
                    f"{self.base_url}/auth/signin",
                    json=signin_data,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    print(f"❌ Could not authenticate with new password")
                    return False
                
                new_token = response.json().get('access_token')
                headers = {
                    "Authorization": f"Bearer {new_token}",
                    "Content-Type": "application/json"
                }
                
                # Change password back
                password_data = {
                    "current_password": self.new_password,
                    "new_password": self.test_password
                }
                
                response = await client.put(
                    f"{self.base_url}/auth/change-password",
                    json=password_data,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    print(f"✅ Password reset back to original")
                    return True
                else:
                    print(f"❌ Failed to reset password: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Password reset error: {str(e)}")
                return False
    
    async def run_all_tests(self):
        """Run all profile and password tests"""
        print("🚀 Starting Profile Update and Password Change Tests...")
        print("=" * 70)
        print(f"📧 Test Email: {self.test_email}")
        print(f"🔑 Current Password: {self.test_password}")
        print(f"🔑 New Password: {self.new_password}")
        print("=" * 70)
        
        # Authenticate first
        if not await self.authenticate():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return False
        
        # Test profile update
        profile_success = await self.test_profile_update()
        
        # Test password change with wrong current password
        wrong_password_success = await self.test_password_change_wrong_current()
        
        # Test password change with correct current password
        password_change_success = await self.test_password_change_correct()
        
        # Test signin with new password
        new_password_signin_success = False
        if password_change_success:
            new_password_signin_success = await self.test_signin_with_new_password()
        
        # Test that old password no longer works
        old_password_rejected_success = False
        if password_change_success:
            old_password_rejected_success = await self.test_signin_with_old_password()
        
        # Reset password back for future tests
        reset_success = False
        if password_change_success:
            reset_success = await self.reset_password_back()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Results Summary:")
        print(f"👤 Profile Update: {'✅ PASS' if profile_success else '❌ FAIL'}")
        print(f"🔐 Wrong Password Rejection: {'✅ PASS' if wrong_password_success else '❌ FAIL'}")
        print(f"🔐 Password Change: {'✅ PASS' if password_change_success else '❌ FAIL'}")
        print(f"🔐 New Password Signin: {'✅ PASS' if new_password_signin_success else '❌ FAIL'}")
        print(f"🔐 Old Password Rejected: {'✅ PASS' if old_password_rejected_success else '❌ FAIL'}")
        print(f"🔄 Password Reset Back: {'✅ PASS' if reset_success else '❌ FAIL'}")
        
        all_passed = (profile_success and wrong_password_success and 
                     password_change_success and new_password_signin_success and 
                     old_password_rejected_success and reset_success)
        
        if all_passed:
            print("\n🎉 All profile and password tests passed!")
        else:
            print("\n⚠️ Some tests failed. Check the details above.")
            
        return all_passed

async def main():
    """Main test function"""
    print("🧪 PROFILE UPDATE & PASSWORD CHANGE TEST SUITE")
    print("=" * 70)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("=" * 70)
    
    # Create tester instance
    tester = ProfileUpdateTester()
    
    # Run all tests
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())