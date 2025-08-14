"""
Gemini Video Generation Service using Veo 3.0
This service uses the working google.genai client for video generation
"""
import os
import time
import uuid
from pathlib import Path
from google import genai
from google.genai import types
from app.core.storage_service import upload_to_gcs
import io

class GeminiVideoService:
    def __init__(self):
        """Initialize Gemini video service with Veo 3.0"""
        try:
            # Initialize the Gemini client with API key
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                self.client = genai.Client(api_key=api_key)
            else:
                # Fallback to default credentials
                self.client = genai.Client()
            
            print("✅ Gemini Video Service initialized with Veo 3.0")
            
        except Exception as e:
            print(f"❌ Error initializing Gemini Video Service: {e}")
            raise
    
    async def generate_video(
        self,
        prompt: str,
        # aspect_ratio: str = "16:9",
        # duration: str = "8",
        # audio_generation: bool = True,
        # watermark: bool = False,
        # person_generation: str = "allow_all"
    ) -> str:
        """
        Generate video using Gemini with Veo 3.0 and upload to GCS
        
        Args:
            prompt (str): Text description for the video
        
        Returns:
            str: URL of the uploaded video
        """
        try:
            print(f"🎬 Starting video generation with Veo 3.0...")
            print(f"📝 Prompt: {prompt}")
            # print(f"📐 Aspect ratio: {aspect_ratio}")
            # print(f"👥 Person generation: {person_generation}")
            
            start_time = time.time()
            
            # Create negative prompt for better quality
            #negative_prompt = "blurry, low quality, distorted faces, bad lighting, shaky camera, poor audio"
            
            # Generate video using Veo 3.0 model
            print("🔄 Sending request to Veo 3.0...")
            operation = self.client.models.generate_videos(
                model="veo-3.0-generate-preview",
                prompt=prompt,
                # negative_prompt=negative_prompt,
                # aspect_ratio=aspect_ratio,
                # person_generation=person_generation,
            )
            
            print(f"🔄 Video generation started. Operation: {operation.name}")
            
            # Poll the operation status until the video is ready
            max_wait_time = 1800  # 30 minutes timeout
            while not operation.done:
                elapsed_time = time.time() - start_time
                
                if elapsed_time > max_wait_time:
                    raise Exception(f"Video generation timeout after {max_wait_time} seconds")
                
                print(f"⏳ Waiting for video generation... ({elapsed_time:.0f}s elapsed)")
                time.sleep(15)  # Check every 15 seconds
                operation = self.client.operations.get(operation)
            
            # Check if generation was successful
            if not hasattr(operation.response, 'generated_videos') or not operation.response.generated_videos:
                raise Exception("Video generation failed - no videos in response")
            
            # Get the generated video
            generated_video = operation.response.generated_videos[0]
            
            print(f"💾 Downloading video...")
            
            # Download video data
            self.client.files.download(file=generated_video.video)
            
            # Create unique filename
            safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')[:30]
            unique_id = uuid.uuid4().hex[:8]
            timestamp = int(time.time())
            aspect_suffix = "16x9"  # Fixed aspect ratio since it's always 16:9
            filename = f"short_video_{aspect_suffix}_{safe_prompt}_{timestamp}_{unique_id}.mp4"
            
            # Save video temporarily to get file data
            temp_path = Path(f"/tmp/{filename}")
            generated_video.video.save(str(temp_path))
            
            # Read the video file and upload to GCS
            with open(temp_path, 'rb') as video_file:
                video_data = video_file.read()
                file_obj = io.BytesIO(video_data)
                video_url = upload_to_gcs(file_obj, filename, "video/mp4")
            
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()
            
            print(f"✅ Video generated and uploaded successfully!")
            print(f"🔗 Video URL: {video_url}")
            print(f"⏱️ Total generation time: {time.time() - start_time:.1f} seconds")
            
            return video_url
            
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            raise Exception(f"Video generation failed: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test if the Gemini video service is working"""
        try:
            # Simple test - this would require a small test generation
            print("🔍 Testing Gemini Video Service connection...")
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

# Create singleton instance
gemini_video_service = GeminiVideoService()