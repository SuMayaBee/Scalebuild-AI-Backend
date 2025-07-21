"""
Enhanced Image Generation Service for Presentations
Supports DALL-E image generation with Google Cloud Storage
"""
import os
import io
import base64
import asyncio
from typing import Optional
from openai import OpenAI
from google.cloud import storage
from datetime import datetime
import uuid

class PresentationImageService:
    def __init__(self):
        from google.oauth2 import service_account

        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.gcs_bucket_name = os.getenv("GCS_BUCKET_NAME", "deck123")

        # Build Google credentials from environment variables
        service_account_info = {
            "type": os.getenv("TYPE"),
            "project_id": os.getenv("PROJECT_ID"),
            "private_key_id": os.getenv("PRIVATE_KEY_ID"),
            "private_key": os.getenv("PRIVATE_KEY"),
            "client_email": os.getenv("CLIENT_EMAIL"),
            "client_id": os.getenv("CLIENT_ID"),
            "auth_uri": os.getenv("AUTH_URI"),
            "token_uri": os.getenv("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
            "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
        }

        # Use centralized GCS client
        from app.core.gcs_client import get_shared_gcs_client
        self.storage_client = get_shared_gcs_client()
        print("✅ Enhanced Image Service: Using credentials from environment variables")

        self.bucket = self.storage_client.bucket(self.gcs_bucket_name)
    
    async def generate_image_dalle3(self, prompt: str, size: str = "1024x1024", filename: str = None) -> str:
        """
        Generate image using DALL-E 3
        Returns the public GCS URL
        """
        try:
            print(f"Generating image with DALL-E 3: {prompt}")
            
            # Generate image with DALL-E 3
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
                response_format="b64_json"
            )
            
            if not response.data or not response.data[0].b64_json:
                raise Exception("No image data received from DALL-E")
            
            # Decode base64 image
            image_data = base64.b64decode(response.data[0].b64_json)
            
            # Use provided filename or generate one
            if filename:
                gcs_filename = filename if filename.startswith("presentation_images/") else f"presentation_images/{filename}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')[:30]
                gcs_filename = f"presentation_images/dalle3_{safe_prompt}_{timestamp}_{unique_id}.png"
            
            # Upload to Google Cloud Storage
            blob = self.bucket.blob(gcs_filename)
            blob.upload_from_string(
                image_data,
                content_type="image/png"
            )
            
            # Make the blob publicly readable
            blob.make_public()
            
            public_url = blob.public_url
            print(f"Image uploaded to GCS: {public_url}")
            
            return public_url
            
        except Exception as e:
            print(f"Error generating image with DALL-E 3: {e}")
            raise e
    
    async def generate_image_dalle2(self, prompt: str, size: str = "1024x1024", filename: str = None) -> str:
        """
        Generate image using DALL-E 2 (fallback option)
        Returns the public GCS URL
        """
        try:
            print(f"Generating image with DALL-E 2: {prompt}")
            
            # Generate image with DALL-E 2
            response = self.openai_client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size=size,
                n=1,
                response_format="b64_json"
            )
            
            if not response.data or not response.data[0].b64_json:
                raise Exception("No image data received from DALL-E 2")
            
            # Decode base64 image
            image_data = base64.b64decode(response.data[0].b64_json)
            
            # Use provided filename or generate one
            if filename:
                gcs_filename = filename if filename.startswith("presentation_images/") else f"presentation_images/{filename}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')[:30]
                gcs_filename = f"presentation_images/dalle2_{safe_prompt}_{timestamp}_{unique_id}.png"
            
            # Upload to Google Cloud Storage
            blob = self.bucket.blob(gcs_filename)
            blob.upload_from_string(
                image_data,
                content_type="image/png"
            )
            
            # Make the blob publicly readable
            blob.make_public()
            
            public_url = blob.public_url
            print(f"Image uploaded to GCS: {public_url}")
            
            return public_url
            
        except Exception as e:
            print(f"Error generating image with DALL-E 2: {e}")
            raise e
    
    async def generate_presentation_image(
        self, 
        prompt: str, 
        model: str = "dalle3",
        size: str = "1024x1024",
        filename: str = None
    ) -> str:
        """
        Main method to generate images for presentations
        Supports model selection: "dalle3" or "dalle2"
        """
        try:
            if model.lower() == "dalle3":
                return await self.generate_image_dalle3(prompt, size, filename)
            elif model.lower() == "dalle2":
                return await self.generate_image_dalle2(prompt, size, filename)
            else:
                # Default to DALL-E 3
                return await self.generate_image_dalle3(prompt, size, filename)
        except Exception as e:
            print(f"Error with {model}, trying fallback...")
            # If DALL-E 3 fails, try DALL-E 2
            if model.lower() == "dalle3":
                try:
                    return await self.generate_image_dalle2(prompt, size, filename)
                except Exception as fallback_error:
                    print(f"Fallback also failed: {fallback_error}")
                    raise e
            else:
                raise e
    
    def test_gcs_connection(self) -> bool:
        """Test Google Cloud Storage connection"""
        try:
            # Try to access the bucket
            bucket_exists = self.bucket.exists()
            print(f"GCS Bucket '{self.gcs_bucket_name}' exists: {bucket_exists}")
            return bucket_exists
        except Exception as e:
            print(f"GCS connection test failed: {e}")
            return False
    
    def test_openai_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            # Try a simple API call
            models = self.openai_client.models.list()
            print("OpenAI connection successful")
            return True
        except Exception as e:
            print(f"OpenAI connection test failed: {e}")
            return False

# Export for import in routes.py and elsewhere
enhanced_image_service = PresentationImageService()