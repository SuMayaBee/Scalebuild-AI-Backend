#!/usr/bin/env python3
"""
Test script for document delete endpoints
"""
import asyncio
import httpx
import json

async def test_document_delete_endpoints():
    """Test all document delete endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🗑️ DOCUMENT DELETE ENDPOINTS TEST")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test individual document deletions
        delete_tests = [
            {
                "name": "Business Proposal",
                "endpoint": "/documents/business-proposal/1",
                "description": "Delete business proposal with ID 1"
            },
            {
                "name": "Partnership Agreement", 
                "endpoint": "/documents/partnership-agreement/1",
                "description": "Delete partnership agreement with ID 1"
            },
            {
                "name": "NDA",
                "endpoint": "/documents/nda/1", 
                "description": "Delete NDA with ID 1"
            },
            {
                "name": "Contract",
                "endpoint": "/documents/contract/1",
                "description": "Delete contract with ID 1"
            },
            {
                "name": "Terms of Service",
                "endpoint": "/documents/terms-of-service/1",
                "description": "Delete terms of service with ID 1"
            },
            {
                "name": "Privacy Policy",
                "endpoint": "/documents/privacy-policy/1",
                "description": "Delete privacy policy with ID 1"
            }
        ]
        
        print("1️⃣ Testing Individual Document Deletions:")
        print("-" * 50)
        
        for test in delete_tests:
            print(f"\n🗑️ {test['name']}")
            print(f"   📝 {test['description']}")
            
            try:
                response = await client.delete(f"{base_url}{test['endpoint']}")
                print(f"   📊 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ {result.get('message')}")
                    print(f"   🆔 Deleted ID: {result.get('deleted_id')}")
                elif response.status_code == 404:
                    print(f"   ℹ️ Document not found (expected if no test data)")
                else:
                    print(f"   ❌ Error: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        # Test bulk deletions for a user
        user_id = 1
        bulk_delete_tests = [
            {
                "name": "All Business Proposals",
                "endpoint": f"/documents/business-proposal/user/{user_id}/all",
                "description": f"Delete all business proposals for user {user_id}"
            },
            {
                "name": "All Partnership Agreements",
                "endpoint": f"/documents/partnership-agreement/user/{user_id}/all",
                "description": f"Delete all partnership agreements for user {user_id}"
            },
            {
                "name": "All NDAs",
                "endpoint": f"/documents/nda/user/{user_id}/all",
                "description": f"Delete all NDAs for user {user_id}"
            },
            {
                "name": "All Contracts",
                "endpoint": f"/documents/contract/user/{user_id}/all",
                "description": f"Delete all contracts for user {user_id}"
            },
            {
                "name": "All Terms of Service",
                "endpoint": f"/documents/terms-of-service/user/{user_id}/all",
                "description": f"Delete all terms of service for user {user_id}"
            },
            {
                "name": "All Privacy Policies",
                "endpoint": f"/documents/privacy-policy/user/{user_id}/all",
                "description": f"Delete all privacy policies for user {user_id}"
            }
        ]
        
        print(f"\n\n2️⃣ Testing Bulk Document Deletions for User {user_id}:")
        print("-" * 50)
        
        for test in bulk_delete_tests:
            print(f"\n🗑️ {test['name']}")
            print(f"   📝 {test['description']}")
            
            try:
                response = await client.delete(f"{base_url}{test['endpoint']}")
                print(f"   📊 Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ {result.get('message')}")
                    print(f"   📊 Deleted Count: {result.get('deleted_count', 0)}")
                else:
                    print(f"   ❌ Error: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        # Test delete ALL documents for a user
        print(f"\n\n3️⃣ Testing Delete ALL Documents for User {user_id}:")
        print("-" * 50)
        
        print(f"\n🗑️ Delete All Documents")
        print(f"   📝 Delete ALL document types for user {user_id}")
        
        try:
            response = await client.delete(f"{base_url}/documents/user/{user_id}/all")
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ {result.get('message')}")
                print(f"   👤 User ID: {result.get('user_id')}")
                print(f"   📊 Total Deleted: {result.get('total_deleted', 0)}")
                print(f"   📋 Breakdown:")
                
                deleted_counts = result.get('deleted_counts', {})
                for doc_type, count in deleted_counts.items():
                    print(f"      • {doc_type.replace('_', ' ').title()}: {count}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

async def test_document_creation_and_deletion():
    """Test creating and then deleting documents"""
    
    base_url = "http://localhost:8000"
    
    print(f"\n\n4️⃣ Testing Document Creation and Deletion Flow:")
    print("-" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Create a test business proposal
        print("\n📝 Creating test business proposal...")
        
        proposal_data = {
            "user_id": 999,  # Use a test user ID
            "company_name": "Test Company",
            "client_name": "Test Client", 
            "project_title": "Test Project",
            "project_description": "A test project for deletion testing",
            "budget": "10000",
            "timeline": "3 months",
            "deliverables": ["Test deliverable 1", "Test deliverable 2"]
        }
        
        try:
            response = await client.post(f"{base_url}/documents/business-proposal", json=proposal_data)
            
            if response.status_code == 200:
                result = response.json()
                proposal_id = result.get('id')
                print(f"   ✅ Created business proposal with ID: {proposal_id}")
                
                # Now delete it
                print(f"   🗑️ Deleting business proposal {proposal_id}...")
                
                delete_response = await client.delete(f"{base_url}/documents/business-proposal/{proposal_id}")
                
                if delete_response.status_code == 200:
                    delete_result = delete_response.json()
                    print(f"   ✅ {delete_result.get('message')}")
                else:
                    print(f"   ❌ Delete failed: {delete_response.text}")
            else:
                print(f"   ❌ Creation failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

async def main():
    """Main test function"""
    print("🧪 DOCUMENT DELETE ENDPOINTS TEST SUITE")
    print("=" * 60)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("=" * 60)
    
    # Test all delete endpoints
    await test_document_delete_endpoints()
    
    # Test creation and deletion flow
    await test_document_creation_and_deletion()
    
    print("\n" + "=" * 60)
    print("🎯 AVAILABLE DELETE ENDPOINTS:")
    print("📋 Individual Document Deletions:")
    print("   DELETE /documents/business-proposal/{id}")
    print("   DELETE /documents/partnership-agreement/{id}")
    print("   DELETE /documents/nda/{id}")
    print("   DELETE /documents/contract/{id}")
    print("   DELETE /documents/terms-of-service/{id}")
    print("   DELETE /documents/privacy-policy/{id}")
    print("")
    print("📋 Bulk Deletions by Document Type:")
    print("   DELETE /documents/business-proposal/user/{user_id}/all")
    print("   DELETE /documents/partnership-agreement/user/{user_id}/all")
    print("   DELETE /documents/nda/user/{user_id}/all")
    print("   DELETE /documents/contract/user/{user_id}/all")
    print("   DELETE /documents/terms-of-service/user/{user_id}/all")
    print("   DELETE /documents/privacy-policy/user/{user_id}/all")
    print("")
    print("📋 Delete ALL Documents:")
    print("   DELETE /documents/user/{user_id}/all")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())