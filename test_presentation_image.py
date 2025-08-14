#!/usr/bin/env python3
"""
Test script for presentation image generation
"""
import asyncio
import httpx
import json

async def test_presentation_image_generation():
    """Test the presentation image generation endpoint"""
    
    base_url = "http://localhost:8000"
    
    print("🖼️ PRESENTATION IMAGE GENERATION TEST")
    print("=" * 60)
    
    # Test image generation requests
    test_cases = [
        {
            "name": "Simple Business Concept",
            "prompt": "modern office building with glass facade in downtown business district",
            "size": "1024x1024"
        },
        {
            "name": "Technology Theme",
            "prompt": "futuristic data center with glowing servers and network connections in blue tones",
            "size": "1792x1024"  # Landscape for presentations
        },
        {
            "name": "Team Collaboration",
            "prompt": "diverse team of professionals collaborating around a conference table with laptops and charts",
            "size": "1024x1024"
        }
    ]
    
    async with httpx.AsyncClient(timeout=120.0) as client:  # Extended timeout for image generation
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}️⃣ Testing: {test_case['name']}")
            print(f"   Prompt: {test_case['prompt']}")
            print(f"   Size: {test_case['size']}")
            
            # Prepare request data
            image_request = {
                "prompt": test_case["prompt"],
                "size": test_case["size"],
                "quality": "hd",
                "context": "presentation slide background"
            }
            
            try:
                print("   🔄 Generating image...")
                
                response = await client.post(
                    f"{base_url}/presentation/generate-image",
                    json=image_request
                )
                
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("success"):
                        print(f"   ✅ Image generated successfully!")
                        print(f"   🔗 URL: {result.get('url')}")
                        print(f"   📝 Model: {result.get('model')}")
                        print(f"   📏 Size: {result.get('size')}")
                        print(f"   📁 Filename: {result.get('filename')}")
                        
                        # Test if the URL is accessible
                        try:
                            image_response = await client.head(result.get('url'))
                            if image_response.status_code == 200:
                                print(f"   ✅ Image URL is accessible")
                            else:
                                print(f"   ⚠️ Image URL returned status: {image_response.status_code}")
                        except Exception as url_error:
                            print(f"   ⚠️ Could not verify image URL: {str(url_error)}")
                    else:
                        print(f"   ❌ Image generation failed: {result.get('error')}")
                else:
                    print(f"   ❌ Request failed: {response.text}")
                    
            except asyncio.TimeoutError:
                print(f"   ⏰ Request timed out (image generation can take time)")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print("   " + "-" * 50)

async def test_image_with_presentation_id():
    """Test image generation linked to a presentation"""
    
    base_url = "http://localhost:8000"
    
    print(f"\n🔗 TESTING IMAGE WITH PRESENTATION LINK")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        
        # Test with a sample presentation ID
        image_request = {
            "prompt": "professional business chart showing growth trends with upward arrows in corporate blue theme",
            "presentation_id": 1,  # Assuming presentation ID 1 exists
            "size": "1792x1024",
            "quality": "hd"
        }
        
        try:
            print("🔄 Generating image linked to presentation...")
            
            response = await client.post(
                f"{base_url}/presentation/generate-image",
                json=image_request
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    print(f"✅ Image generated and linked to presentation!")
                    print(f"🔗 URL: {result.get('url')}")
                    print(f"📝 Model: {result.get('model')}")
                    print(f"📏 Size: {result.get('size')}")
                    print(f"📁 Filename: {result.get('filename')}")
                    
                    # Try to get images for the presentation
                    print(f"\n🔍 Checking presentation images...")
                    images_response = await client.get(f"{base_url}/presentation/1/images")
                    
                    if images_response.status_code == 200:
                        images = images_response.json()
                        print(f"✅ Found {len(images)} images for presentation")
                        for img in images[-3:]:  # Show last 3 images
                            print(f"   - {img.get('prompt')[:50]}...")
                    else:
                        print(f"⚠️ Could not retrieve presentation images: {images_response.status_code}")
                else:
                    print(f"❌ Image generation failed: {result.get('error')}")
            else:
                print(f"❌ Request failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")

async def test_service_connections():
    """Test the underlying service connections"""
    
    print(f"\n🔧 TESTING SERVICE CONNECTIONS")
    print("=" * 60)
    
    try:
        # Import the service directly
        import sys
        sys.path.append('.')
        from app.presentation.service.enhanced_image_service import enhanced_image_service
        
        print("1️⃣ Testing OpenAI connection...")
        openai_ok = enhanced_image_service.test_openai_connection()
        print(f"   OpenAI: {'✅ Connected' if openai_ok else '❌ Failed'}")
        
        print("\n2️⃣ Testing Google Cloud Storage connection...")
        gcs_ok = enhanced_image_service.test_gcs_connection()
        print(f"   GCS: {'✅ Connected' if gcs_ok else '❌ Failed'}")
        
        if openai_ok and gcs_ok:
            print(f"\n✅ All service connections are working!")
            return True
        else:
            print(f"\n⚠️ Some service connections failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing service connections: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🧪 PRESENTATION IMAGE GENERATION TEST SUITE")
    print("=" * 60)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("⚠️  NOTE: Image generation can take 10-30 seconds per image")
    print("=" * 60)
    
    # Test service connections first
    connections_ok = await test_service_connections()
    
    if connections_ok:
        # Test basic image generation
        await test_presentation_image_generation()
        
        # Test image with presentation linking
        await test_image_with_presentation_id()
    else:
        print("\n⚠️ Skipping image generation tests due to connection issues")
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("✅ If images generated successfully, check the URLs in browser")
    print("✅ Images should be stored in Google Cloud Storage")
    print("✅ Database should have presentation_images records")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())