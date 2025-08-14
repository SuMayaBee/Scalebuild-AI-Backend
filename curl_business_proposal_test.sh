#!/bin/bash
# Business Proposal CRUD Test using curl commands
# Make sure your server is running: uvicorn app.main:app --reload

echo "📋 BUSINESS PROPOSAL CRUD TEST WITH CURL"
echo "========================================"

BASE_URL="http://localhost:8000"
USER_ID=1

# Step 1: Create a business proposal
echo ""
echo "1️⃣ Creating business proposal..."
RESPONSE=$(curl -s -X POST "$BASE_URL/documents/business-proposal" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "company_name": "TechSolutions Inc.",
    "client_name": "Global Enterprises Ltd.",
    "project_title": "Digital Transformation Initiative",
    "project_description": "A comprehensive digital transformation project.",
    "services_offered": [
      "Cloud Migration Services",
      "Custom Software Development",
      "Data Analytics Implementation"
    ],
    "timeline": "6 months",
    "budget_range": "$50,000 - $75,000",
    "contact_person": "John Smith",
    "contact_email": "john.smith@techsolutions.com"
  }')

# Extract proposal ID
PROPOSAL_ID=$(echo $RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ ! -z "$PROPOSAL_ID" ]; then
    echo "✅ Created proposal with ID: $PROPOSAL_ID"
    
    # Step 2: Read the proposal
    echo ""
    echo "2️⃣ Reading proposal $PROPOSAL_ID..."
    curl -s -X GET "$BASE_URL/documents/business-proposal/$PROPOSAL_ID" | jq '.project_title, .company_name, .client_name'
    
    # Step 3: Update the proposal
    echo ""
    echo "3️⃣ Updating proposal $PROPOSAL_ID..."
    curl -s -X PUT "$BASE_URL/documents/business-proposal/$PROPOSAL_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "ai_generated_content": "UPDATED: This is the updated business proposal content with enhanced details and new information."
      }' | jq '.message // "Updated successfully"'
    
    # Step 4: Delete the proposal
    echo ""
    echo "4️⃣ Deleting proposal $PROPOSAL_ID..."
    curl -s -X DELETE "$BASE_URL/documents/business-proposal/$PROPOSAL_ID" | jq '.message'
    
    # Step 5: Verify deletion
    echo ""
    echo "5️⃣ Verifying deletion..."
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/documents/business-proposal/$PROPOSAL_ID")
    
    if [ "$HTTP_CODE" = "404" ]; then
        echo "✅ Deletion verified (404 Not Found)"
    else
        echo "❌ Proposal still exists (HTTP $HTTP_CODE)"
    fi
    
else
    echo "❌ Failed to create proposal"
    echo "Response: $RESPONSE"
fi

echo ""
echo "🎯 CRUD Test Complete!"
echo "========================================"