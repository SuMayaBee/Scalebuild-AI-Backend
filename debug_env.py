"""
Debug script to check environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Environment Variables Check:")
print(f"RESEND_API_KEY: {'✅ Set' if os.getenv('RESEND_API_KEY') else '❌ Not set'}")
print(f"SENDER_EMAIL: {os.getenv('SENDER_EMAIL', 'Not set')}")
print(f"SENDER_NAME: {os.getenv('SENDER_NAME', 'Not set')}")

# Check if API key starts with 're_'
api_key = os.getenv('RESEND_API_KEY')
if api_key:
    print(f"API Key format: {'✅ Valid' if api_key.startswith('re_') else '❌ Invalid'}")
    print(f"API Key length: {len(api_key)} characters")
else:
    print("❌ No API key found")

# Test Resend import
try:
    import resend
    print("✅ Resend package imported successfully")
    
    # Set API key and test
    if api_key:
        resend.api_key = api_key
        print("✅ API key set in resend package")
except ImportError:
    print("❌ Resend package not installed")
except Exception as e:
    print(f"❌ Error with resend package: {e}")