"""
Centralized Google Cloud Storage Client
"""
import os
from google.cloud import storage
from google.oauth2 import service_account


def get_gcs_client():
    """
    Get a properly configured GCS client using environment variables.
    
    Returns:
        storage.Client: Configured GCS client
    """
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

    # Remove any None values
    service_account_info = {k: v for k, v in service_account_info.items() if v is not None}

    try:
        # Fix the private key formatting (replace \\n with actual newlines)
        if service_account_info.get("private_key"):
            service_account_info["private_key"] = service_account_info["private_key"].replace('\\n', '\n')
        
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        client = storage.Client(credentials=credentials, project=service_account_info.get("project_id"))
        return client
        
    except Exception as e:
        print(f"Failed to load Google credentials from env: {e}")
        raise Exception(f"Could not load GCS credentials from environment variables: {e}")


# Global client instance (lazy loaded)
_gcs_client = None

def get_shared_gcs_client():
    """
    Get a shared GCS client instance (singleton pattern).
    
    Returns:
        storage.Client: Shared GCS client
    """
    global _gcs_client
    if _gcs_client is None:
        _gcs_client = get_gcs_client()
    return _gcs_client