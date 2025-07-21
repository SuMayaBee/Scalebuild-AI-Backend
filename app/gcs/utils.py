from typing import Tuple
import re
from urllib.parse import urlparse


class GCSURLParser:
    """Utility class for parsing and validating Google Cloud Storage URLs."""
    
    @staticmethod
    def parse_gcs_url(url: str) -> Tuple[str, str]:
        """
        Parse a GCS URL and extract bucket name and file path.
        Supports both gs:// and https://storage.googleapis.com/ formats.
        
        Args:
            url: GCS URL in format:
                - gs://bucket-name/path/to/file
                - https://storage.googleapis.com/bucket-name/path/to/file
            
        Returns:
            Tuple of (bucket_name, file_path)
            
        Raises:
            ValueError: If URL format is invalid
        """
        if not isinstance(url, str):
            raise ValueError('URL must be a string')
        
        if url.startswith('gs://'):
            return GCSURLParser._parse_gs_url(url)
        elif url.startswith('https://storage.googleapis.com/'):
            return GCSURLParser._parse_https_url(url)
        else:
            raise ValueError('URL must start with gs:// or https://storage.googleapis.com/')
    
    @staticmethod
    def _parse_gs_url(url: str) -> Tuple[str, str]:
        """Parse gs:// format URL."""
        # Remove gs:// prefix
        url_without_prefix = url[5:]
        
        if not url_without_prefix:
            raise ValueError('URL cannot be empty after gs:// prefix')
        
        # Split into bucket and path components
        parts = url_without_prefix.split('/', 1)
        
        if len(parts) < 2 or not parts[1]:
            raise ValueError('URL must include both bucket name and file path (gs://bucket/path)')
        
        bucket_name = parts[0]
        file_path = parts[1]
        
        # Validate bucket name and file path
        GCSURLParser._validate_bucket_name(bucket_name)
        GCSURLParser._validate_file_path(file_path)
        
        return bucket_name, file_path
    
    @staticmethod
    def _parse_https_url(url: str) -> Tuple[str, str]:
        """Parse https://storage.googleapis.com/ format URL."""
        parsed = urlparse(url)
        
        if parsed.netloc != 'storage.googleapis.com':
            raise ValueError('HTTPS URL must use storage.googleapis.com domain')
        
        if not parsed.path or parsed.path == '/':
            raise ValueError('URL must include both bucket name and file path')
        
        # Remove leading slash and split path
        path_parts = parsed.path.lstrip('/').split('/', 1)
        
        if len(path_parts) < 2 or not path_parts[1]:
            raise ValueError('URL must include both bucket name and file path')
        
        bucket_name = path_parts[0]
        file_path = path_parts[1]
        
        # Validate bucket name and file path
        GCSURLParser._validate_bucket_name(bucket_name)
        GCSURLParser._validate_file_path(file_path)
        
        return bucket_name, file_path
    
    @staticmethod
    def _validate_bucket_name(bucket_name: str) -> None:
        """Validate GCS bucket name according to basic naming rules."""
        if not bucket_name:
            raise ValueError('Bucket name cannot be empty')
        
        if len(bucket_name) < 3 or len(bucket_name) > 63:
            raise ValueError('Bucket name must be between 3 and 63 characters')
        
        # Basic bucket name validation (alphanumeric, hyphens, dots)
        # Must start and end with alphanumeric character
        if not re.match(r'^[a-z0-9][a-z0-9\-\.]*[a-z0-9]$', bucket_name):
            raise ValueError('Invalid bucket name format')
        
        # Cannot contain consecutive dots
        if '..' in bucket_name:
            raise ValueError('Bucket name cannot contain consecutive dots')
        
        # Cannot start with 'goog' or contain 'google'
        if bucket_name.startswith('goog') or 'google' in bucket_name.lower():
            raise ValueError('Bucket name cannot start with "goog" or contain "google"')
    
    @staticmethod
    def _validate_file_path(file_path: str) -> None:
        """Validate GCS file path format."""
        if not file_path:
            raise ValueError('File path cannot be empty')
        
        if file_path.startswith('/') or file_path.endswith('/'):
            raise ValueError('File path cannot start or end with slash')
        
        # Check for invalid characters (basic validation)
        invalid_chars = ['\\', '\0', '\r', '\n']
        for char in invalid_chars:
            if char in file_path:
                raise ValueError(f'File path cannot contain invalid character: {repr(char)}')