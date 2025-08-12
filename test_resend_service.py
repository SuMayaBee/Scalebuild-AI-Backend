"""
Test script for Resend Email Service
Run this script to test the Resend email functionality
"""
import asyncio
import httpx
import json
from typing import Dict, Any


class ResendEmailTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.auth_token = None
    
    async def authenticate(self, email: str, password: str) -> bool:
        """Authenticate and get access token"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    data={"username": email, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.auth_token = data.get("access_token")
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
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    async def test_health_check(self):
        """Test Resend service health check"""
        print("\n🔍 Testing Resend Health Check...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/resend/health")
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Health check error: {str(e)}")
    
    async def test_available_templates(self):
        """Test getting available templates"""
        print("\n📋 Testing Available Templates...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/resend/templates")
                print(f"Status: {response.status_code}")
                print(f"Available Templates: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Templates error: {str(e)}")
    
    async def test_send_custom_email(self, to_email: str):
        """Test sending a custom email"""
        print(f"\n📧 Testing Custom Email to {to_email}...")
        
        email_data = {
            "to_email": to_email,
            "subject": "Test Email from ScalebuildAI Resend Service",
            "html_content": """
            <html>
            <body>
                <h2>🚀 Test Email from ScalebuildAI</h2>
                <p>This is a test email sent using the <strong>Resend API</strong>!</p>
                <p>Features tested:</p>
                <ul>
                    <li>✅ HTML content rendering</li>
                    <li>✅ Custom styling</li>
                    <li>✅ Emoji support 🎉</li>
                </ul>
                <p>If you received this email, the Resend integration is working perfectly!</p>
                <hr>
                <p><em>Sent from ScalebuildAI Test Suite</em></p>
            </body>
            </html>
            """,
            "text_content": "This is a test email from ScalebuildAI using Resend API. If you received this, the integration is working!",
            "tags": [{"name": "test", "value": "custom_email"}]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/resend/send",
                    headers=self.get_headers(),
                    json=email_data,
                    timeout=30.0
                )
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Custom email error: {str(e)}")
    
    async def test_welcome_email(self, to_email: str, name: str = "Test User"):
        """Test sending a welcome email"""
        print(f"\n🎉 Testing Welcome Email to {to_email}...")
        
        email_data = {
            "to_email": to_email,
            "name": name
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/resend/welcome",
                    headers=self.get_headers(),
                    json=email_data,
                    timeout=30.0
                )
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Welcome email error: {str(e)}")
    
    async def test_contact_form_email(self, to_email: str):
        """Test sending a contact form email"""
        print(f"\n📞 Testing Contact Form Email to {to_email}...")
        
        email_data = {
            "to_email": to_email,
            "sender_name": "John Doe",
            "sender_email": "john.doe@example.com",
            "subject": "Inquiry about ScalebuildAI Services",
            "message": "Hi there! I'm interested in learning more about your AI-powered business tools. Could you please provide more information about pricing and features? Thanks!"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/resend/contact",
                    headers={"Content-Type": "application/json"},
                    json=email_data,
                    timeout=30.0
                )
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Contact form email error: {str(e)}")
    
    async def test_password_reset_email(self, to_email: str, name: str = "Test User"):
        """Test sending a password reset email"""
        print(f"\n🔐 Testing Password Reset Email to {to_email}...")
        
        email_data = {
            "to_email": to_email,
            "name": name,
            "reset_token": "test_reset_token_123456",
            "reset_url": "https://scalebuild-new.vercel.app/reset-password?token=test_reset_token_123456"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/resend/password-reset",
                    headers=self.get_headers(),
                    json=email_data,
                    timeout=30.0
                )
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            except Exception as e:
                print(f"❌ Password reset email error: {str(e)}")
    
    async def run_all_tests(self, test_email: str, auth_email: str = None, auth_password: str = None):
        """Run all email tests"""
        print("🚀 Starting Resend Email Service Tests...")
        print(f"Test email recipient: {test_email}")
        
        # Test health check (no auth required)
        await self.test_health_check()
        
        # Test available templates (no auth required)
        await self.test_available_templates()
        
        # Test contact form (no auth required)
        await self.test_contact_form_email(test_email)
        
        # If authentication credentials provided, test authenticated endpoints
        if auth_email and auth_password:
            print(f"\n🔐 Attempting authentication with {auth_email}...")
            if await self.authenticate(auth_email, auth_password):
                await self.test_send_custom_email(test_email)
                await self.test_welcome_email(test_email, "Test User")
                await self.test_password_reset_email(test_email, "Test User")
            else:
                print("⚠️ Skipping authenticated tests due to authentication failure")
        else:
            print("⚠️ No authentication credentials provided. Skipping authenticated tests.")
            print("   To test authenticated endpoints, provide auth_email and auth_password")
        
        print("\n✅ All tests completed!")


async def main():
    """Main test function"""
    # Configuration
    TEST_EMAIL = "your-test-email@example.com"  # Replace with your test email
    AUTH_EMAIL = "your-auth-email@example.com"  # Replace with your auth email (optional)
    AUTH_PASSWORD = "your-password"  # Replace with your password (optional)
    
    print("=" * 60)
    print("🧪 RESEND EMAIL SERVICE TEST SUITE")
    print("=" * 60)
    print("⚠️  IMPORTANT: Make sure to:")
    print("   1. Set RESEND_API_KEY in your .env file")
    print("   2. Update TEST_EMAIL with a real email address")
    print("   3. Start your FastAPI server (uvicorn app.main:app --reload)")
    print("   4. Optionally provide AUTH_EMAIL and AUTH_PASSWORD for authenticated tests")
    print("=" * 60)
    
    # Create tester instance
    tester = ResendEmailTester()
    
    # Run tests
    await tester.run_all_tests(
        test_email=TEST_EMAIL,
        auth_email=AUTH_EMAIL if AUTH_EMAIL != "your-auth-email@example.com" else None,
        auth_password=AUTH_PASSWORD if AUTH_PASSWORD != "your-password" else None
    )


if __name__ == "__main__":
    asyncio.run(main())