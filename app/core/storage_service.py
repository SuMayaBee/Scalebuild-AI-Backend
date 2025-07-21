"""
Generic Google Cloud Storage Service
"""
import os
import io
from typing import Optional
from app.core.gcs_client import get_shared_gcs_client

class StorageService:
    def __init__(self):
        self.gcs_bucket_name = os.getenv("GCS_BUCKET_NAME", "deck123")
        self.storage_client = get_shared_gcs_client()
        self.bucket = self.storage_client.bucket(self.gcs_bucket_name)
        print("✅ Storage Service: Using credentials from environment variables")

def upload_to_gcs(file_obj: io.BytesIO, filename: str, content_type: str, bucket_name: Optional[str] = None) -> str:
    """
    Upload a file to Google Cloud Storage and return the public URL
    
    Args:
        file_obj: File-like object containing the data
        filename: Name of the file in GCS
        content_type: MIME type of the file
        bucket_name: Optional bucket name, uses default if not provided
    
    Returns:
        Public URL of the uploaded file
    """
    try:
        storage_service = StorageService()
        
        # Use provided bucket or default
        if bucket_name:
            bucket = storage_service.storage_client.bucket(bucket_name)
        else:
            bucket = storage_service.bucket
        
        # Create blob and upload
        blob = bucket.blob(filename)
        file_obj.seek(0)  # Reset file pointer to beginning
        
        blob.upload_from_file(
            file_obj,
            content_type=content_type
        )
        
        # Make the blob publicly accessible
        blob.make_public()
        
        public_url = blob.public_url
        print(f"File uploaded to GCS: {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        raise e