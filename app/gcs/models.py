from pydantic import BaseModel, Field, validator
from typing import Optional
from .utils import GCSURLParser


class GCSDownloadRequest(BaseModel):
    file_url: str = Field(..., description="Google Cloud Storage file URL (gs://bucket/path or https://storage.googleapis.com/bucket/path)")
    
    @validator('file_url')
    def validate_gcs_url(cls, v):
        # Use the GCSURLParser for consistent validation
        try:
            GCSURLParser.parse_gcs_url(v)
        except ValueError as e:
            raise ValueError(str(e))
        return v


class GCSDownloadResponse(BaseModel):
    success: bool = True
    filename: str
    content_type: str
    size_bytes: Optional[int] = None


class GCSErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: str