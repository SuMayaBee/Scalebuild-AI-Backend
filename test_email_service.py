#!/usr/bin/env python3
"""
Test script for email service
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_email_endpoints():
    """Test all email endpoints"""
    
    print("🚀 Testing Email Service")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n🔍 Test 1: Email service health check...")
    try:
        response = requests.get(f"{BASE_URL}/email/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Email service health check passed!")
            print(f"Status: {health_data['status']}")
            print(f"Configured: {health_data['configured']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Contact form (no authentication required)
    print("\n🔍 Test 2: Contact form email...")
    contact_data = {
        "to_email": "recipient@example.com",
        "sender_name": "John Doe",
        "sender_email": "john@example.com",
        "subject": "Test Contact Message",
        "message": "This is a test message from the contact form."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/email/contact", json=contact_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Contact email test passed!")
            print(f"Message: {result['message']}")
            print(f"Recipient: {result['recipient']}")
        else:
            print(f"❌ Contact email failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Contact email error: {e}")
    
    # Test 3: Custom email (requires authentication)
    print("\n🔍 Test 3: Custom email (requires authentication)...")
    
    # First, get authentication token
    signin_data = {
        "email": "user123456@example.com",  # Use existing user
        "password": "testpass123"
    }
    
    try:
        signin_response = requests.post(f"{BASE_URL}/auth/signin", json=signin_data)
        if signin_response.status_code == 200:
            token = signin_response.json()['access_token']
            print(f"✅ Authentication successful!")
            
            # Send custom email
            custom_email_data = {
                "to_email": "recipient@example.com",
                "subject": "Custom Email Test",
                "message": "This is a custom email sent through the API.",
                "html_message": "<h2>Custom Email Test</h2><p>This is a <strong>custom email</strong> sent through the API.</p>"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            email_response = requests.post(f"{BASE_URL}/email/send", json=custom_email_data, headers=headers)
            
            if email_response.status_code == 200:
                result = email_response.json()
                print("✅ Custom email test passed!")
                print(f"Message: {result['message']}")
                print(f"Recipient: {result['recipient']}")
            else:
                print(f"❌ Custom email failed: {email_response.status_code}")
                print(email_response.text)
                
        else:
            print(f"❌ Authentication failed: {signin_response.status_code}")
            print("Note: Make sure you have a user account created first")
            
    except Exception as e:
        print(f"❌ Custom email test error: {e}")
    
    # Test 4: Welcome email (requires authentication)
    print("\n🔍 Test 4: Welcome email...")
    try:
        if 'token' in locals():
            welcome_data = {
                "to_email": "newuser@example.com",
                "name": "New User"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            welcome_response = requests.post(f"{BASE_URL}/email/welcome", json=welcome_data, headers=headers)
            
            if welcome_response.status_code == 200:
                result = welcome_response.json()
                print("✅ Welcome email test passed!")
                print(f"Message: {result['message']}")
                print(f"Recipient: {result['recipient']}")
            else:
                print(f"❌ Welcome email failed: {welcome_response.status_code}")
                print(welcome_response.text)
        else:
            print("⏭️ Skipping welcome email test (no authentication token)")
            
    except Exception as e:
        print(f"❌ Welcome email test error: {e}")

if __name__ == "__main__":
    test_email_endpoints()