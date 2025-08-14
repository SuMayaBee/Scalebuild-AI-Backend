#!/usr/bin/env python3
"""
Test script for short video generation using Gemini with Veo 3.0
"""
import asyncio
import httpx
import json

async def test_short_video_generation():
    """Test the short video generation endpoint"""
    
    base_url = "http://localhost:8000"
    
    print("🎬 SHORT VIDEO GENERATION TEST")
    print("=" * 60)
    
    # Test cases with different prompts
    test_cases = [
        {
            "user_id": 1,
            "prompt": "A close up of two cats staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"
        },
        {
            "user_id": 1,
            "prompt": "A beautiful sunset over the ocean with waves gently crashing on the shore, seagulls flying overhead"
        },
        {
            "user_id": 1,
            "prompt": "A bustling city street at night with neon lights reflecting on wet pavement, people walking with umbrellas"
        }
    ]
    
    async with httpx.AsyncClient(timeout=1800.0) as client:  # 30 minute timeout for video generation
        
        # First, test the health check
        print("1️⃣ Testing service health check...")
        try:
            response = await client.get(f"{base_url}/short-video/status/check")
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Service Status: {health_data.get('status')}")
                print(f"   🎬 Service: {health_data.get('service')}")
                print(f"   🤖 Model: {health_data.get('model')}")
                print(f"   📋 Fixed Settings: {health_data.get('fixed_settings')}")
            else:
                print(f"   ❌ Health check failed: {response.text}")
                return
                
        except Exception as e:
            print(f"   ❌ Health check error: {str(e)}")
            return
        
        print("\n" + "=" * 60)
        
        # Test video generation with the first test case
        test_case = test_cases[0]  # Use the first test case
        
        print(f"2️⃣ Testing video generation...")
        print(f"   👤 User ID: {test_case['user_id']}")
        print(f"   📝 Prompt: {test_case['prompt'][:80]}...")
        
        try:
            print("   🔄 Sending video generation request...")
            
            response = await client.post(
                f"{base_url}/short-video/generate",
                json=test_case
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Video generated successfully!")
                print(f"   🆔 Video ID: {result.get('id')}")
                print(f"   🔗 Video URL: {result.get('video_url')}")
                print(f"   📐 Aspect Ratio: {result.get('aspect_ratio')}")
                print(f"   ⏱️ Duration: {result.get('duration')}")
                print(f"   🎵 Audio Generation: {result.get('audio_generation')}")
                print(f"   💧 Watermark: {result.get('watermark')}")
                print(f"   👥 Person Generation: {result.get('person_generation')}")
                print(f"   📅 Created At: {result.get('created_at')}")
                
                # Test retrieving the video
                video_id = result.get('id')
                if video_id:
                    print(f"\n3️⃣ Testing video retrieval...")
                    
                    retrieve_response = await client.get(f"{base_url}/short-video/{video_id}")
                    
                    if retrieve_response.status_code == 200:
                        retrieved_video = retrieve_response.json()
                        print(f"   ✅ Video retrieved successfully!")
                        print(f"   📝 Retrieved Prompt: {retrieved_video.get('prompt')[:50]}...")
                    else:
                        print(f"   ❌ Video retrieval failed: {retrieve_response.text}")
                
                # Test getting user videos
                print(f"\n4️⃣ Testing user videos retrieval...")
                
                user_videos_response = await client.get(f"{base_url}/short-video/user/{test_case['user_id']}")
                
                if user_videos_response.status_code == 200:
                    user_videos = user_videos_response.json()
                    print(f"   ✅ User videos retrieved successfully!")
                    print(f"   📊 Total videos for user: {len(user_videos)}")
                    
                    for i, video in enumerate(user_videos[-3:], 1):  # Show last 3 videos
                        print(f"   {i}. ID: {video.get('id')} - {video.get('prompt')[:40]}...")
                else:
                    print(f"   ❌ User videos retrieval failed: {user_videos_response.text}")
                
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
                print(f"   ❌ Video generation failed: {error_detail}")
                
        except asyncio.TimeoutError:
            print(f"   ⏰ Request timed out (video generation can take 10-30 minutes)")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

async def test_multiple_prompts():
    """Test multiple video generation prompts"""
    
    base_url = "http://localhost:8000"
    
    print("\n🎬 MULTIPLE PROMPTS TEST")
    print("=" * 60)
    
    prompts = [
        "A serene mountain lake at sunrise with mist rising from the water",
        "Colorful paint drops falling into clear water in slow motion",
        "A cozy coffee shop with people reading books and soft lighting"
    ]
    
    async with httpx.AsyncClient(timeout=1800.0) as client:
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}️⃣ Testing prompt {i}: {prompt[:50]}...")
            
            test_data = {
                "user_id": 1,
                "prompt": prompt
            }
            
            try:
                response = await client.post(
                    f"{base_url}/short-video/generate",
                    json=test_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Success! Video ID: {result.get('id')}")
                    print(f"   🔗 URL: {result.get('video_url')}")
                else:
                    print(f"   ❌ Failed: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            # Small delay between requests
            if i < len(prompts):
                print("   ⏸️ Waiting 30 seconds before next generation...")
                await asyncio.sleep(30)

async def main():
    """Main test function"""
    print("🧪 SHORT VIDEO GENERATION TEST SUITE")
    print("=" * 60)
    print("⚠️  IMPORTANT: Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("⚠️  NOTE: Video generation can take 10-30 minutes per video")
    print("=" * 60)
    
    choice = input("\nChoose test:\n1. Single video generation test\n2. Multiple prompts test\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        await test_short_video_generation()
    elif choice == "2":
        await test_multiple_prompts()
    else:
        print("Invalid choice. Running single video test...")
        await test_short_video_generation()
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY:")
    print("✅ If videos generated successfully, check the video URLs")
    print("✅ Videos should be stored in Google Cloud Storage")
    print("✅ Database should have short_videos records")
    print("✅ Request format: {user_id: int, prompt: string}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())