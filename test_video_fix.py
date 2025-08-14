#!/usr/bin/env python3
"""
Quick test to verify the video generation fix
"""
import asyncio
import httpx

async def test_video_generation_fix():
    """Test that the video generation fix works"""
    
    base_url = "http://localhost:8000"
    
    print("🔧 TESTING VIDEO GENERATION FIX")
    print("=" * 50)
    
    # Simple test request
    test_request = {
        "user_id": 1,
        "prompt": "A cute cat playing with a ball of yarn"
    }
    
    async with httpx.AsyncClient(timeout=1800.0) as client:
        
        print("1️⃣ Testing service health...")
        try:
            response = await client.get(f"{base_url}/short-video/status/check")
            if response.status_code == 200:
                health = response.json()
                print(f"   ✅ Service: {health.get('service')}")
                print(f"   📊 Status: {health.get('status')}")
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
                return
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
            return
        
        print("\n2️⃣ Testing video generation...")
        print(f"   📝 Prompt: {test_request['prompt']}")
        
        try:
            response = await client.post(
                f"{base_url}/short-video/generate",
                json=test_request
            )
            
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Video generation started successfully!")
                print(f"   🆔 Video ID: {result.get('id')}")
                print(f"   🔗 Video URL: {result.get('video_url')}")
                print(f"   📐 Aspect Ratio: {result.get('aspect_ratio')}")
                print(f"   ⏱️ Duration: {result.get('duration')}")
                print(f"   🎵 Audio: {result.get('audio_generation')}")
                print(f"   💧 Watermark: {result.get('watermark')}")
                print(f"   👥 Person Gen: {result.get('person_generation')}")
                
                print(f"\n   🎉 Fix successful! Video generation is working.")
                
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type') == 'application/json' else response.text
                print(f"   ❌ Video generation failed: {error_detail}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 QUICK VIDEO GENERATION FIX TEST")
    print("=" * 50)
    print("⚠️  Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload")
    print("=" * 50)
    
    asyncio.run(test_video_generation_fix())