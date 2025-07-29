#!/usr/bin/env python3
"""
Set CORS configuration for GCS bucket using Python
"""
import json
from dotenv import load_dotenv
from app.core.gcs_client import get_shared_gcs_client

def set_bucket_cors():
    """Set CORS configuration for the GCS bucket."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get GCS client
        client = get_shared_gcs_client()
        bucket_name = "deck123"
        bucket = client.bucket(bucket_name)
        
        # Read CORS configuration
        with open('cors.json', 'r') as f:
            cors_data = json.load(f)
        
        # Extract the cors array from the JSON structure
        cors_config = cors_data.get('cors', [])
        
        # Set CORS configuration
        bucket.cors = cors_config
        bucket.patch()
        
        print(f"✅ CORS configuration set successfully for bucket: {bucket_name}")
        print(f"CORS rules: {json.dumps(cors_config, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error setting CORS: {e}")

if __name__ == "__main__":
    set_bucket_cors()