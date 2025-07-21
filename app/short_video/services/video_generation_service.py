import os
import json
import requests
import time
import base64
import uuid
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.cloud import storage
from app.core.storage_service import upload_to_gcs
import io

# CONFIGURATION
PROJECT_ID = "intrepid-stock-394612"  # Veo project ID
LOCATION_ID = "us-central1"
API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
MODEL_ID = "veo-3.0-generate-preview"
GCS_BUCKET_NAME = "deck123"

class VideoGenerationService:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.location_id = LOCATION_ID
        self.api_endpoint = API_ENDPOINT
        self.model_id = MODEL_ID
        self.gcs_bucket_name = GCS_BUCKET_NAME
        
        # Build Google credentials from environment variables (for Veo service)
        self.veo_service_account_info = {
            "type": os.getenv("VEO_TYPE"),
            "project_id": os.getenv("VEO_PROJECT_ID"),
            "private_key_id": os.getenv("VEO_PRIVATE_KEY_ID"),
            "private_key": os.getenv("VEO_PRIVATE_KEY"),
            "client_email": os.getenv("VEO_CLIENT_EMAIL"),
            "client_id": os.getenv("VEO_CLIENT_ID"),
            "auth_uri": os.getenv("VEO_AUTH_URI"),
            "token_uri": os.getenv("VEO_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("VEO_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("VEO_CLIENT_X509_CERT_URL"),
            "universe_domain": os.getenv("VEO_UNIVERSE_DOMAIN"),
        }

        # Remove any None values (in case some env vars are missing)
        self.veo_service_account_info = {k: v for k, v in self.veo_service_account_info.items() if v is not None}
        
        # Initialize credentials
        try:
            self.credentials = service_account.Credentials.from_service_account_info(
                self.veo_service_account_info,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            print("Veo credentials loaded from environment variables")
        except Exception as e:
            print(f"Failed to load Veo credentials from environment variables: {e}")
            # Fallback to default credentials if available
            try:
                self.credentials = service_account.Credentials.from_service_account_file(
                    "key2.json",
                    scopes=["https://www.googleapis.com/auth/cloud-platform"],
                )
                print("Fallback: Veo credentials loaded from key2.json")
            except Exception as fallback_error:
                print(f"Failed to load fallback credentials: {fallback_error}")
                raise Exception("Could not load Veo service account credentials")
    
    def get_access_token(self):
        """Get OAuth2 access token"""
        self.credentials.refresh(Request())
        return self.credentials.token
    
    async def generate_video(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        duration: str = "8",
        audio_generation: bool = True,
        watermark: bool = True,
        person_generation: str = "allow_all"
    ):
        """Generate video using Veo 3.0 model and upload to GCS"""
        try:
            # Get access token
            access_token = self.get_access_token()
            
            # Build the request payload
            payload = {
                "endpoint": f"projects/{self.project_id}/locations/{self.location_id}",
                "instances": [
                    {"prompt": prompt}
                ],
                "parameters": {
                    "aspectRatio": aspect_ratio,
                    "sampleCount": 1,  # Generate 1 video
                    "durationSeconds": duration,
                    "personGeneration": person_generation,
                    "addWatermark": watermark,
                    "includeRaiReason": True,
                    "generateAudio": audio_generation
                }
            }
            
            # Make the REST API call
            url = f"https://{self.api_endpoint}/v1/projects/{self.project_id}/locations/{self.location_id}/publishers/google/models/{self.model_id}:predictLongRunning"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                raise Exception(f"API call failed with status {response.status_code}: {response.text}")
            
            resp_json = response.json()
            
            if "name" not in resp_json:
                raise Exception("No operation name returned from API")
            
            # Poll for operation completion and get video
            video_url = await self._poll_and_upload_video(resp_json["name"], access_token, prompt)
            
            return video_url
            
        except Exception as e:
            print(f"Error in video generation: {e}")
            raise e
    
    async def _poll_and_upload_video(self, operation_name: str, access_token: str, prompt: str):
        """Poll for operation completion and upload video to GCS"""
        fetch_url = f"https://{self.api_endpoint}/v1/projects/{self.project_id}/locations/{self.location_id}/publishers/google/models/{self.model_id}:fetchPredictOperation"
        fetch_payload = {"operationName": operation_name}
        fetch_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        max_attempts = 30  # Maximum polling attempts (10 minutes)
        attempt = 0
        
        while attempt < max_attempts:
            try:
                fetch_resp = requests.post(fetch_url, headers=fetch_headers, json=fetch_payload)
                
                if fetch_resp.status_code != 200:
                    print(f"Fetch operation failed with status {fetch_resp.status_code}")
                    time.sleep(20)
                    attempt += 1
                    continue
                
                fetch_json = fetch_resp.json()
                
                # Check if video data is available
                video_datas = []
                if fetch_json and "response" in fetch_json:
                    if "videos" in fetch_json["response"]:
                        video_datas = fetch_json["response"]["videos"]
                    elif "video" in fetch_json["response"]:
                        video_datas = [fetch_json["response"]["video"]]
                
                if video_datas:
                    # Process the first video
                    video_dict = video_datas[0]
                    
                    # Extract base64 string from dict
                    if isinstance(video_dict, dict):
                        video_b64 = video_dict.get('bytesBase64Encoded')
                        if not video_b64:
                            raise Exception(f"No base64 data found in video dict: {video_dict}")
                    else:
                        video_b64 = video_dict
                    
                    # Decode video data
                    video_data = base64.b64decode(video_b64)
                    
                    # Create unique filename
                    safe_prompt = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).strip()
                    safe_prompt = safe_prompt.replace(' ', '_')[:30]
                    unique_id = uuid.uuid4().hex[:8]
                    filename = f"short_video_{safe_prompt}_{unique_id}.mp4"
                    
                    # Upload to GCS
                    file_obj = io.BytesIO(video_data)
                    video_url = upload_to_gcs(file_obj, filename, "video/mp4")
                    
                    print(f"Video generated and uploaded successfully: {video_url}")
                    return video_url
                
                else:
                    print(f"No video data found yet. Attempt {attempt + 1}/{max_attempts}. Waiting 20 seconds...")
                    time.sleep(20)
                    attempt += 1
                    
            except Exception as e:
                print(f"Error during polling attempt {attempt + 1}: {e}")
                time.sleep(20)
                attempt += 1
        
        raise Exception("Video generation timed out after maximum polling attempts")

# Create a singleton instance
video_generation_service = VideoGenerationService()