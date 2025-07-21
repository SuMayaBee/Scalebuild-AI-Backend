import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/msi/Desktop/Aladin AI/Scalable AI/backend/veo-crafter/key1.json"

import json
import requests
import time
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.cloud import storage

# CONFIGURATION
SERVICE_ACCOUNT_FILE = "key2.json"  # Path to your service account key
PROJECT_ID = "intrepid-stock-394612"  # Replace with your GCP project ID
LOCATION_ID = "us-central1"
API_ENDPOINT = "us-central1-aiplatform.googleapis.com"
MODEL_ID = "veo-3.0-generate-preview"  # Use the correct model for your use case
GCS_BUCKET_NAME = "deck123"  # Use the same bucket as in video_gen.py

# 1. Get OAuth2 access token using service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
credentials.refresh(Request())
access_token = credentials.token

# 2. Build the request payload
prompt = "A cat is flying with ballons"  # Replace with your prompt
payload = {
    "endpoint": f"projects/{PROJECT_ID}/locations/{LOCATION_ID}",
    "instances": [
        {"prompt": prompt}
    ],
    "parameters": {
        "aspectRatio": "16:9",
        "sampleCount": 2,
        "durationSeconds": "8",
        "personGeneration": "allow_all",
        "addWatermark": True,
        "includeRaiReason": True,
        "generateAudio": True
    }
}

# 3. Make the REST API call
url = f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/{LOCATION_ID}/publishers/google/models/{MODEL_ID}:predictLongRunning"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
try:
    resp_json = response.json()
    print("Response:", resp_json)
except Exception:
    print("Response Text:", response.text)
    resp_json = None

# 4. Poll for operation status and download/upload video(s)
def upload_to_gcs(local_file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    blob.make_public()
    print(f"Uploaded to GCS: {blob.public_url}")
    return blob.public_url

if resp_json and "name" in resp_json:
    operation_name = resp_json["name"]
    fetch_url = f"https://{API_ENDPOINT}/v1/projects/{PROJECT_ID}/locations/{LOCATION_ID}/publishers/google/models/{MODEL_ID}:fetchPredictOperation"
    fetch_payload = {"operationName": operation_name}
    fetch_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    import base64
    while True:
        fetch_resp = requests.post(fetch_url, headers=fetch_headers, json=fetch_payload)
        print("FetchPredictOperation status:", fetch_resp.status_code)
        try:
            fetch_json = fetch_resp.json()
            print("FetchPredictOperation response:", fetch_json)
        except Exception:
            print("FetchPredictOperation response text:", fetch_resp.text)
            fetch_json = None
        video_datas = []
        if fetch_json and "response" in fetch_json:
            if "videos" in fetch_json["response"]:
                video_datas = fetch_json["response"]["videos"]
            elif "video" in fetch_json["response"]:
                video_datas = [fetch_json["response"]["video"]]
        if video_datas:
            for idx, video_dict in enumerate(video_datas):
                # Extract base64 string from dict if needed
                if isinstance(video_dict, dict):
                    video_b64 = video_dict.get('bytesBase64Encoded')
                    if not video_b64:
                        print(f"No base64 data found in video dict: {video_dict}")
                        continue
                else:
                    video_b64 = video_dict
                local_path = f"video_{idx}.mp4"
                with open(local_path, "wb") as f:
                    f.write(base64.b64decode(video_b64))
                print(f"Decoded and saved video to {local_path}")
                # Upload to GCS
                gcs_url = upload_to_gcs(local_path, GCS_BUCKET_NAME, f"veo_videos/{local_path}")
                print(f"Video uploaded to GCS: {gcs_url}")
            break
        else:
            print("No base64 video data found yet. Waiting 20 seconds before retrying...")
            time.sleep(20)
