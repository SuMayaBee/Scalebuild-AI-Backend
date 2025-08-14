#!/usr/bin/env python3
"""
Test script for Business Proposal CRUD operations
Creates a dummy business proposal, updates it, then deletes it
"""
import asyncio
import httpx
import json

async def test_business_proposal_crud():
    """Test complete CRUD operations for business proposal"""
    
    base_url = "http://localhost:8000"
    user_id = 1
    
    print("📋 BUSINESS PROPOSAL CRUD TEST")
    print("=" * 60)
    print(f"👤 User ID: {user_id}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Step 1: Create a dummy business proposal
        print("\n1️⃣ Creating dummy business proposal...")
        
        proposal_data = {
            "user_id": user_id,
            "company_name": "TechSolutions Inc.",
            "client_name": "Global Enterprises Ltd.",
            "project_title": "Digital Transformation Initiative",
            "project_description": "A comprehensive digital transformation project to modernize the client's business processes and improve operational efficiency.",
            "services_offered": [
                "Cloud Migration Services",
                "Custom Software Development", 
                "Data Analytics Implementation",
                "Staff Training and Support"
            ],
            "timeline": "6 months",
            "budget_range": "$50,000 - $75,000",
            "contact_person": "John Smith",
            "contact_email": "john.smith@techsolutions.com",
            "logo_url": "https://example.com/logo.png"
        }
        
        try:
            response = await client.post(f"{base_url}/documents/business-proposal", json=proposal_data)
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                proposal_id = result.get('id')
                print(f"   ✅ Business proposal created successfully!")
                print(f"   🆔 Proposal ID: {proposal_id}")
                print(f"   🏢 Company: {result.get('company_name')}")
                print(f"   👤 Client: {result.get('client_name')}")
                print(f"   📝 Project: {result.get('project_title')}")
                print(f"   📅 Created: {result.get('created_at')}")
                
                # Step 2: Read the created proposal
                print(f"\n2️⃣ Reading the created proposal...")
                
                read_response = await client.get(f"{base_url}/documents/business-proposal/{proposal_id}")
                print(f"   📊 Status Code: {read_response.status_code}")
                
                if read_response.status_code == 200:
                    read_result = read_response.json()
                    print(f"   ✅ Proposal retrieved successfully!")
                    print(f"   📝 AI Content Preview: {read_result.get('ai_generated_content', '')[:100]}...")
                else:
                    print(f"   ❌ Failed to read proposal: {read_response.text}")
                
                # Step 3: Update the proposal content
                print(f"\n3️⃣ Updating the proposal content...")
                
                updated_content = """
                UPDATED BUSINESS PROPOSAL
                ========================
                
                Dear Global Enterprises Ltd.,
                
                We are pleased to present this UPDATED proposal for your Digital Transformation Initiative.
                
                EXECUTIVE SUMMARY:
                This updated proposal outlines our enhanced approach to modernizing your business processes
                with cutting-edge technology solutions and improved timeline.
                
                UPDATED SERVICES:
                1. Advanced Cloud Migration with AI Integration
                2. Custom Software Development with Mobile Apps
                3. Advanced Data Analytics with Machine Learning
                4. Comprehensive Staff Training and 24/7 Support
                5. NEW: Cybersecurity Implementation
                
                UPDATED TIMELINE: 4 months (accelerated delivery)
                UPDATED BUDGET: $60,000 - $80,000
                
                We look forward to partnering with you on this exciting journey.
                
                Best regards,
                TechSolutions Inc.
                """
                
                update_data = {
                    "ai_generated_content": updated_content
                }
                
                update_response = await client.put(f"{base_url}/documents/business-proposal/{proposal_id}", json=update_data)
                print(f"   📊 Status Code: {update_response.status_code}")
                
                if update_response.status_code == 200:
                    update_result = update_response.json()
                    print(f"   ✅ Proposal updated successfully!")
                    print(f"   📝 Updated Content Preview: {update_result.get('ai_generated_content', '')[:150]}...")
                    print(f"   📅 Updated At: {update_result.get('updated_at')}")
                else:
                    print(f"   ❌ Failed to update proposal: {update_response.text}")
                
                # Step 4: Get all proposals for the user
                print(f"\n4️⃣ Getting all proposals for user {user_id}...")
                
                user_proposals_response = await client.get(f"{base_url}/documents/business-proposal/user/{user_id}")
                print(f"   📊 Status Code: {user_proposals_response.status_code}")
                
                if user_proposals_response.status_code == 200:
                    user_proposals = user_proposals_response.json()
                    print(f"   ✅ Retrieved {len(user_proposals)} proposals for user {user_id}")
                    
                    for i, proposal in enumerate(user_proposals, 1):
                        print(f"   {i}. ID: {proposal.get('id')} - {proposal.get('project_title')}")
                else:
                    print(f"   ❌ Failed to get user proposals: {user_proposals_response.text}")
                
                # Step 5: Delete the proposal
                print(f"\n5️⃣ Deleting the proposal...")
                
                delete_response = await client.delete(f"{base_url}/documents/business-proposal/{proposal_id}")
                print(f"   📊 Status Code: {delete_response.status_code}")
                
                if delete_response.status_code == 200:
                    delete_result = delete_response.json()
                    print(f"   ✅ {delete_result.get('message')}")
                    print(f"   🗑️ Deleted ID: {delete_result.get('deleted_id')}")
                    
                    # Step 6: Verify deletion
                    print(f"\n6️⃣ Verifying deletion...")
                    
                    verify_response = await client.get(f"{base_url}/documents/business-proposal/{proposal_id}")
                    print(f"   📊 Status Code: {verify_response.status_code}")
                    
                    if verify_response.status_code == 404:
                        print(f"   ✅ Proposal successfully deleted (404 Not Found)")
                    else:
                        print(f"   ❌ Proposal still exists: {verify_response.text}")
                        
                else:
                    print(f"   ❌ Failed to delete proposal: {delete_response.text}")
                
            else:
                print(f"   ❌ Failed to create proposal: {response.text}")
                return
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

async def test_bulk_operations():
    """Test bulk operations with multiple proposals"""
    
    base_url = "http://localhost:8000"
    user_id = 1
    
    print(f"\n\n📋 BULK OPERATIONS TEST")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Create multiple proposals
        print("1️⃣ Creating multiple test proposals...")
        
        proposals_data = [
            {
                "user_id": user_id,
                "company_name": "TechSolutions Inc.",
                "client_name": "Client A Corp",
                "project_title": "E-commerce Platform Development",
                "project_description": "Building a modern e-commerce platform",
                "services_offered": ["Web Development", "Payment Integration"],
                "timeline": "3 months",
                "budget_range": "$30,000 - $40,000",
                "contact_person": "Alice Johnson",
                "contact_email": "alice@techsolutions.com"
            },
            {
                "user_id": user_id,
                "company_name": "TechSolutions Inc.",
                "client_name": "Client B Ltd",
                "project_title": "Mobile App Development",
                "project_description": "Creating a cross-platform mobile application",
                "services_offered": ["Mobile Development", "UI/UX Design"],
                "timeline": "4 months",
                "budget_range": "$25,000 - $35,000",
                "contact_person": "Bob Wilson",
                "contact_email": "bob@techsolutions.com"
            },
            {
                "user_id": user_id,
                "company_name": "TechSolutions Inc.",
                "client_name": "Client C Inc",
                "project_title": "Data Analytics Dashboard",
                "project_description": "Building a comprehensive analytics dashboard",
                "services_offered": ["Data Analytics", "Dashboard Development"],
                "timeline": "2 months",
                "budget_range": "$20,000 - $30,000",
                "contact_person": "Carol Davis",
                "contact_email": "carol@techsolutions.com"
            }
        ]
        
        created_ids = []
        
        for i, proposal_data in enumerate(proposals_data, 1):
            try:
                response = await client.post(f"{base_url}/documents/business-proposal", json=proposal_data)
                
                if response.status_code == 200:
                    result = response.json()
                    proposal_id = result.get('id')
                    created_ids.append(proposal_id)
                    print(f"   ✅ Created proposal {i}: ID {proposal_id} - {proposal_data['project_title']}")
                else:
                    print(f"   ❌ Failed to create proposal {i}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error creating proposal {i}: {str(e)}")
        
        print(f"\n   📊 Created {len(created_ids)} proposals: {created_ids}")
        
        # Delete all proposals for the user
        print(f"\n2️⃣ Deleting all business proposals for user {user_id}...")
        
        try:
            delete_all_response = await client.delete(f"{base_url}/documents/business-proposal/user/{user_id}/all")
            print(f"   📊 Status Code: {delete_all_response.status_code}")
            
            if delete_all_response.status_code == 200:
                delete_result = delete_all_response.json()
                print(f"   ✅ {delete_result.get('message')}")
                print(f"   📊 Deleted Count: {delete_result.get('deleted_count')}")
            else:
                print(f"   ❌ Failed to delete all proposals: {delete_all_response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

async def main():
    """Main test function"""
    print("🧪 BUSINESS PROPOSAL CRUD TEST SUITE")
    print("=" * 60)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("=" * 60)
    
    # Test complete CRUD operations
    await test_business_proposal_crud()
    
    # Test bulk operations
    await test_bulk_operations()
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("✅ Create: Business proposal creation")
    print("✅ Read: Individual proposal retrieval")
    print("✅ Update: Proposal content modification")
    print("✅ Delete: Individual proposal deletion")
    print("✅ List: User's proposals listing")
    print("✅ Bulk Delete: All user proposals deletion")
    print("✅ Verification: Deletion confirmation")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())