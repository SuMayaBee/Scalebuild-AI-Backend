#!/usr/bin/env python3
"""
Test script to demonstrate the improved password reset flow with better UX
"""
import asyncio
import httpx
import json
from typing import Dict, Any

class ImprovedPasswordResetTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_email = "alissaedword82@gmail.com"
        self.current_password = "forget"
        self.new_password = "mynewpassword123"
        self.reset_token = None
    
    async def test_forgot_password(self) -> bool:
        """Test sending forgot password email"""
        print(f"\n📧 Step 1: Requesting password reset for {self.test_email}...")
        
        forgot_data = {
            "email": self.test_email
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/forgot-password",
                    json=forgot_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Password reset email sent!")
                    print(f"📧 Message: {result.get('msg')}")
                    print("📬 Check the server logs for the reset token (in real app, user gets it via email)")
                    return True
                else:
                    print(f"❌ Failed to send reset email: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error sending reset email: {str(e)}")
                return False
    
    async def simulate_getting_token_from_email(self) -> str:
        """Simulate getting the token from email (in real scenario, user gets this from email)"""
        print(f"\n📬 Step 2: Simulating user receiving token from email...")
        
        # In a real scenario, the user would get this token from their email
        # For testing, we'll simulate this by generating a token and setting it in the database
        
        # First, let's trigger a forgot password to get a real token
        forgot_data = {"email": self.test_email}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/auth/forgot-password", json=forgot_data)
            
            if response.status_code == 200:
                print("✅ Reset token generated and sent to email")
                print("💡 In real scenario: User receives token via email")
                print("💡 For testing: Check server logs for the 4-digit token")
                
                # For demo purposes, let's use a sample token
                # In real testing, you'd get this from the server logs
                sample_token = "1234"  # Replace with actual token from logs
                print(f"🔑 Using sample token for demo: {sample_token}")
                return sample_token
            else:
                print("❌ Failed to generate reset token")
                return None
    
    async def test_validate_reset_token(self, token: str) -> bool:
        """Test validating the reset token (Step 1 of improved UX)"""
        print(f"\n🔍 Step 3: Validating reset token: {token}")
        
        validate_data = {
            "token": token
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/validate-reset-token",
                    json=validate_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Token is valid!")
                    print(f"👤 User: {result['user']['name']} ({result['user']['email']})")
                    print(f"📝 Message: {result['message']}")
                    print("💡 Frontend can now show password reset form")
                    return True
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"❌ Token validation failed: {error_detail}")
                    print("💡 Frontend should show 'Invalid or expired token' message")
                    return False
                    
            except Exception as e:
                print(f"❌ Error validating token: {str(e)}")
                return False
    
    async def test_validate_invalid_token(self) -> bool:
        """Test validating an invalid token"""
        print(f"\n🔍 Step 3b: Testing invalid token validation...")
        
        validate_data = {
            "token": "9999"  # Invalid token
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/validate-reset-token",
                    json=validate_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 400:
                    error_detail = response.json().get('detail')
                    print(f"✅ Correctly rejected invalid token: {error_detail}")
                    return True
                else:
                    print(f"❌ Should have rejected invalid token: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error testing invalid token: {str(e)}")
                return False
    
    async def test_reset_password_with_valid_token(self, token: str) -> bool:
        """Test resetting password with validated token (Step 2 of improved UX)"""
        print(f"\n🔐 Step 4: Resetting password with validated token...")
        
        reset_data = {
            "token": token,
            "new_password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/reset-password",
                    json=reset_data,
                    timeout=30.0
                )
                
                print(f"Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Password reset successful!")
                    print(f"📝 Message: {result['message']}")
                    print(f"👤 User: {result['user']['name']} ({result['user']['email']})")
                    return True
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    print(f"❌ Password reset failed: {error_detail}")
                    return False
                    
            except Exception as e:
                print(f"❌ Error resetting password: {str(e)}")
                return False
    
    async def test_signin_with_new_password(self) -> bool:
        """Test signing in with the new password"""
        print(f"\n🔐 Step 5: Testing signin with new password...")
        
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
                    print(f"🔑 Access Token: {token_data.get('access_token', '')[:50]}...")
                    return True
                else:
                    print(f"❌ Signin with new password failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Signin error: {str(e)}")
                return False
    
    async def test_signin_with_old_password(self) -> bool:
        """Test that old password no longer works"""
        print(f"\n🔐 Step 6: Verifying old password no longer works...")
        
        signin_data = {
            "email": self.test_email,
            "password": self.current_password  # Old password
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
                print(f"❌ Error testing old password: {str(e)}")
                return False
    
    async def reset_password_back(self) -> bool:
        """Reset password back to original for future tests"""
        print(f"\n🔄 Step 7: Resetting password back to original...")
        
        # First authenticate with new password
        signin_data = {
            "email": self.test_email,
            "password": self.new_password
        }
        
        async with httpx.AsyncClient() as client:
            try:
                # Get new token
                response = await client.post(f"{self.base_url}/auth/signin", json=signin_data)
                
                if response.status_code != 200:
                    print(f"❌ Could not authenticate with new password")
                    return False
                
                new_token = response.json().get('access_token')
                headers = {
                    "Authorization": f"Bearer {new_token}",
                    "Content-Type": "application/json"
                }
                
                # Change password back using change-password endpoint
                password_data = {
                    "current_password": self.new_password,
                    "new_password": self.current_password
                }
                
                response = await client.put(
                    f"{self.base_url}/auth/change-password",
                    json=password_data,
                    headers=headers
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
    
    async def run_improved_flow_demo(self):
        """Run the complete improved password reset flow demo"""
        print("🚀 IMPROVED PASSWORD RESET FLOW DEMONSTRATION")
        print("=" * 80)
        print("This demonstrates the improved UX for password reset:")
        print("1. User requests password reset")
        print("2. User receives token via email")
        print("3. Frontend validates token before showing reset form")
        print("4. User enters new password and submits")
        print("5. Password is reset successfully")
        print("=" * 80)
        
        # Step 1: Request password reset
        forgot_success = await self.test_forgot_password()
        
        if not forgot_success:
            print("❌ Cannot proceed without successful forgot password request")
            return False
        
        # Step 2: Simulate getting token from email
        token = await self.simulate_getting_token_from_email()
        
        if not token:
            print("❌ Cannot proceed without reset token")
            return False
        
        # Step 3: Validate token (good UX - shows user info)
        validate_success = await self.test_validate_reset_token(token)
        
        # Step 3b: Test invalid token validation
        invalid_token_success = await self.test_validate_invalid_token()
        
        # Step 4: Reset password with validated token
        reset_success = False
        if validate_success:
            reset_success = await self.test_reset_password_with_valid_token(token)
        
        # Step 5: Test new password works
        new_password_success = False
        if reset_success:
            new_password_success = await self.test_signin_with_new_password()
        
        # Step 6: Test old password doesn't work
        old_password_rejected = False
        if reset_success:
            old_password_rejected = await self.test_signin_with_old_password()
        
        # Step 7: Reset back for future tests
        reset_back_success = False
        if reset_success:
            reset_back_success = await self.reset_password_back()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 IMPROVED PASSWORD RESET FLOW RESULTS:")
        print(f"📧 Forgot Password Request: {'✅ PASS' if forgot_success else '❌ FAIL'}")
        print(f"🔍 Token Validation (Valid): {'✅ PASS' if validate_success else '❌ FAIL'}")
        print(f"🔍 Token Validation (Invalid): {'✅ PASS' if invalid_token_success else '❌ FAIL'}")
        print(f"🔐 Password Reset: {'✅ PASS' if reset_success else '❌ FAIL'}")
        print(f"🔐 New Password Signin: {'✅ PASS' if new_password_success else '❌ FAIL'}")
        print(f"🔐 Old Password Rejected: {'✅ PASS' if old_password_rejected else '❌ FAIL'}")
        print(f"🔄 Password Reset Back: {'✅ PASS' if reset_back_success else '❌ FAIL'}")
        
        all_passed = (forgot_success and validate_success and invalid_token_success and 
                     reset_success and new_password_success and old_password_rejected and 
                     reset_back_success)
        
        print("\n" + "=" * 80)
        print("🎯 IMPROVED UX BENEFITS:")
        print("✅ Token validation before password reset form")
        print("✅ User sees their name/email when token is valid")
        print("✅ Clear error messages for invalid tokens")
        print("✅ Separate validation step improves user confidence")
        print("✅ Better error handling and user feedback")
        print("=" * 80)
        
        if all_passed:
            print("\n🎉 All improved password reset flow tests passed!")
        else:
            print("\n⚠️ Some tests failed. Check the details above.")
            
        return all_passed

async def main():
    """Main test function"""
    print("🧪 IMPROVED PASSWORD RESET FLOW TEST SUITE")
    print("=" * 80)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("⚠️  NOTE: Check server logs for the actual 4-digit reset token")
    print("=" * 80)
    
    # Create tester instance
    tester = ImprovedPasswordResetTester()
    
    # Run the improved flow demo
    await tester.run_improved_flow_demo()

if __name__ == "__main__":
    asyncio.run(main())