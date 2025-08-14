#!/usr/bin/env python3
"""
Simple Business Proposal CRUD Test
Creates, updates, and deletes a business proposal for user ID 1
"""
import asyncio
import httpx
import json

async def simple_crud_test():
    """Simple CRUD test with better error handling"""
    
    base_url = "http://localhost:8000"
    user_id = 1
    
    print("📋 SIMPLE BUSINESS PROPOSAL CRUD TEST")
    print("=" * 50)
    
    # Test data
    proposal_data = {
        "user_id": user_id,
        "company_name": "TechSolutions Inc.",
        "client_name": "Global Enterprises Ltd.",
        "project_title": "Digital Transformation Initiative",
        "project_description": "A comprehensive digital transformation project to modernize business processes.",
        "services_offered": [
            "Cloud Migration Services",
            "Custom Software Development", 
            "Data Analytics Implementation"
        ],
        "timeline": "6 months",
        "budget_range": "$50,000 - $75,000",
        "contact_person": "John Smith",
        "contact_email": "john.smith@techsolutions.com"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        try:
            # Step 1: Create
            print("\n1️⃣ Creating business proposal...")
            response = await client.post(f"{base_url}/documents/business-proposal", json=proposal_data)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                proposal_id = result.get('id')
                print(f"✅ Created! ID: {proposal_id}")
                print(f"📝 Project: {result.get('project_title')}")
                
                # Step 2: Read
                print(f"\n2️⃣ Reading proposal {proposal_id}...")
                read_response = await client.get(f"{base_url}/documents/business-proposal/{proposal_id}")
                
                if read_response.status_code == 200:
                    print("✅ Read successful!")
                    read_data = read_response.json()
                    print(f"📄 Content length: {len(read_data.get('ai_generated_content', ''))}")
                
                # Step 3: Update
                print(f"\n3️⃣ Updating proposal {proposal_id}...")
                update_data = {
                    "ai_generated_content": "UPDATED: This is the updated business proposal content with new information and enhanced details."
                }
                
                update_response = await client.put(f"{base_url}/documents/business-proposal/{proposal_id}", json=update_data)
                
                if update_response.status_code == 200:
                    print("✅ Update successful!")
                    update_result = update_response.json()
                    print(f"📝 Updated content: {update_result.get('ai_generated_content')[:50]}...")
                
                # Step 4: Delete
                print(f"\n4️⃣ Deleting proposal {proposal_id}...")
                delete_response = await client.delete(f"{base_url}/documents/business-proposal/{proposal_id}")
                
                if delete_response.status_code == 200:
                    delete_result = delete_response.json()
                    print(f"✅ {delete_result.get('message')}")
                    print(f"🗑️ Deleted ID: {delete_result.get('deleted_id')}")
                    
                    # Step 5: Verify deletion
                    print(f"\n5️⃣ Verifying deletion...")
                    verify_response = await client.get(f"{base_url}/documents/business-proposal/{proposal_id}")
                    
                    if verify_response.status_code == 404:
                        print("✅ Deletion verified (404 Not Found)")
                    else:
                        print(f"❌ Still exists: {verify_response.status_code}")
                else:
                    print(f"❌ Delete failed: {delete_response.status_code} - {delete_response.text}")
            else:
                print(f"❌ Create failed: {response.status_code}")
                print(f"Error: {response.text}")
                
        except httpx.TimeoutException:
            print("❌ Request timed out - check if server is running")
        except httpx.ConnectError:
            print("❌ Connection failed - make sure server is running on http://localhost:8000")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Simple Business Proposal CRUD Test")
    print("Make sure your server is running: uvicorn app.main:app --reload")
    print("=" * 50)
    
    asyncio.run(simple_crud_test())