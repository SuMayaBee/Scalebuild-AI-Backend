"""
Google Cloud Storage Download Service
"""
import io
from typing import Tuple, Optional
from google.api_core import exceptions
from app.core.gcs_client import get_shared_gcs_client
from ..utils import GCSURLParser


class GCSDownloadService:
    def __init__(self):
        self.storage_client = get_shared_gcs_client()
        print("✅ GCS Download Service: Using credentials from environment variables")

    def download_file(self, gcs_url: str) -> Tuple[io.BytesIO, str, str, int]:
        """
        Download a file from Google Cloud Storage.
        
        Args:
            gcs_url: GCS URL in format gs://bucket-name/path/to/file
            
        Returns:
            Tuple of (file_content, filename, content_type, size_bytes)
            
        Raises:
            ValueError: If URL format is invalid
            FileNotFoundError: If file doesn't exist
            PermissionError: If access is denied
            Exception: For other GCS errors
        """
        try:
            # Parse and validate the GCS URL
            bucket_name, file_path = GCSURLParser.parse_gcs_url(gcs_url)
            
            # Get the bucket and blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            
            # Check if the blob exists
            if not blob.exists():
                raise FileNotFoundError(f"File not found: {gcs_url}")
            
            # Download the file content
            file_content = io.BytesIO()
            blob.download_to_file(file_content)
            file_content.seek(0)  # Reset pointer to beginning
            
            # Get file metadata
            blob.reload()  # Refresh metadata
            filename = file_path.split('/')[-1]  # Extract filename from path
            content_type = blob.content_type or 'application/octet-stream'
            size_bytes = blob.size or 0
            
            return file_content, filename, content_type, size_bytes
            
        except ValueError as e:
            # URL parsing errors
            raise ValueError(f"Invalid GCS URL: {str(e)}")
        except exceptions.NotFound:
            raise FileNotFoundError(f"File not found: {gcs_url}")
        except exceptions.Forbidden:
            raise PermissionError(f"Access denied to file: {gcs_url}")
        except Exception as e:
            raise Exception(f"Error downloading file from GCS: {str(e)}")

    def get_file_info(self, gcs_url: str) -> dict:
        """
        Get file information without downloading the content.
        
        Args:
            gcs_url: GCS URL in format gs://bucket-name/path/to/file
            
        Returns:
            Dictionary with file information
        """
        try:
            bucket_name, file_path = GCSURLParser.parse_gcs_url(gcs_url)
            
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            
            if not blob.exists():
                raise FileNotFoundError(f"File not found: {gcs_url}")
            
            blob.reload()  # Refresh metadata
            
            return {
                "filename": file_path.split('/')[-1],
                "content_type": blob.content_type or 'application/octet-stream',
                "size_bytes": blob.size or 0,
                "created": blob.time_created.isoformat() if blob.time_created else None,
                "updated": blob.updated.isoformat() if blob.updated else None,
                "etag": blob.etag,
                "md5_hash": blob.md5_hash
            }
            
        except ValueError as e:
            raise ValueError(f"Invalid GCS URL: {str(e)}")
        except exceptions.NotFound:
            raise FileNotFoundError(f"File not found: {gcs_url}")
        except exceptions.Forbidden:
            raise PermissionError(f"Access denied to file: {gcs_url}")
        except Exception as e:
            raise Exception(f"Error getting file info from GCS: {str(e)}")