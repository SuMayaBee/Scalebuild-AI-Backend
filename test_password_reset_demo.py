#!/usr/bin/env python3
"""
Simple demo of the improved password reset flow
"""
import asyncio
import httpx

async def demo_password_reset_flow():
    """Demo the complete password reset flow"""
    
    base_url = "http://localhost:8000"
    test_email = "alissaedword82@gmail.com"
    
    print("🔐 PASSWORD RESET FLOW DEMO")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # Step 1: Request password reset
        print("1️⃣ Requesting password reset...")
        forgot_data = {"email": test_email}
        response = await client.post(f"{base_url}/auth/forgot-password", json=forgot_data)
        
        if response.status_code == 200:
            print("✅ Password reset email sent!")
            print("📧 Check server logs for the 4-digit token")
        else:
            print(f"❌ Failed: {response.text}")
            return
        
        # Step 2: Test token validation with a sample token
        print("\n2️⃣ Testing token validation...")
        
        # Let's test with some common tokens that might be generated
        test_tokens = ["1234", "5678", "9999", "0000"]
        
        for token in test_tokens:
            print(f"   Testing token: {token}")
            validate_data = {"token": token}
            response = await client.post(f"{base_url}/auth/validate-reset-token", json=validate_data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Token {token} is valid!")
                print(f"   👤 User: {result['user']['name']} ({result['user']['email']})")
                
                # Step 3: Reset password with valid token
                print(f"\n3️⃣ Resetting password with token {token}...")
                reset_data = {
                    "token": token,
                    "new_password": "newpassword123"
                }
                
                response = await client.post(f"{base_url}/auth/reset-password", json=reset_data)
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Password reset successful!")
                    print(f"📝 {result['message']}")
                    
                    # Step 4: Test new password
                    print("\n4️⃣ Testing new password...")
                    signin_data = {
                        "email": test_email,
                        "password": "newpassword123"
                    }
                    
                    response = await client.post(f"{base_url}/auth/signin", json=signin_data)
                    
                    if response.status_code == 200:
                        print("✅ New password works!")
                        
                        # Reset back to original
                        print("\n5️⃣ Resetting back to original password...")
                        token_data = response.json()
                        access_token = token_data.get('access_token')
                        
                        headers = {
                            "Authorization": f"Bearer {access_token}",
                            "Content-Type": "application/json"
                        }
                        
                        change_data = {
                            "current_password": "newpassword123",
                            "new_password": "forget"
                        }
                        
                        response = await client.put(
                            f"{base_url}/auth/change-password",
                            json=change_data,
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            print("✅ Password reset back to original")
                        else:
                            print(f"❌ Failed to reset back: {response.text}")
                    else:
                        print(f"❌ New password doesn't work: {response.text}")
                else:
                    print(f"❌ Password reset failed: {response.text}")
                
                return  # Exit after successful test
            else:
                print(f"   ❌ Token {token} is invalid")
        
        print("\n💡 None of the test tokens worked.")
        print("💡 Check the server logs for the actual 4-digit token generated.")
        print("💡 Then test manually with:")
        print('   curl -X POST "http://localhost:8000/auth/validate-reset-token" \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"token": "YOUR_ACTUAL_TOKEN"}\'')

if __name__ == "__main__":
    asyncio.run(demo_password_reset_flow())