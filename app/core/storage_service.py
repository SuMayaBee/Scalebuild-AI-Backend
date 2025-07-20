"""
Generic Google Cloud Storage Service
"""
import os
import io
from typing import Optional
from google.cloud import storage
from google.oauth2 import service_account

class StorageService:
    def __init__(self):
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

        # Remove any None values (in case some env vars are missing)
        service_account_info = {k: v for k, v in service_account_info.items() if v is not None}

        try:
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            self.storage_client = storage.Client(credentials=credentials, project=service_account_info.get("project_id"))
        except Exception as e:
            print(f"Failed to load Google credentials from env, falling back to default: {e}")
            self.storage_client = storage.Client()

        self.bucket = self.storage_client.bucket(self.gcs_bucket_name)

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