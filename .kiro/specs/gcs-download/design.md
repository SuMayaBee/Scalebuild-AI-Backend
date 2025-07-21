# Design Document

## Overview

The GCS Download feature will provide a REST API endpoint that accepts Google Cloud Storage file URLs and returns the file content as a downloadable response. The implementation will leverage the existing StorageService infrastructure and follow the established FastAPI patterns used throughout the application.

The feature will be implemented as a standalone module that can be easily integrated into the existing application architecture without disrupting current functionality.

## Architecture

### High-Level Flow
1. Client sends POST request with GCS file URL
2. URL validation and parsing to extract bucket and file path
3. Authentication with Google Cloud Storage using existing credentials
4. File retrieval from GCS bucket
5. Stream file content back to client with appropriate headers

### Integration Points
- **Existing StorageService**: Extend current GCS integration for download operations
- **FastAPI Router**: New router following existing patterns in `/app/*/routes.py`
- **Error Handling**: Consistent with application's HTTPException patterns
- **Authentication**: Leverage existing GCS service account credentials

## Components and Interfaces

### 1. GCS Download Router (`app/gcs/routes.py`)
```python
@router.post("/gcs/download")
async def download_from_gcs(request: GCSDownloadRequest) -> StreamingResponse
```

**Input Model:**
```python
class GCSDownloadRequest(BaseModel):
    file_url: str  # Full GCS URL (gs://bucket-name/path/to/file)
```

**Response:**
- StreamingResponse with file content
- Appropriate Content-Type header based on file extension
- Content-Disposition header for download filename

### 2. GCS Download Service (`app/gcs/services/download_service.py`)
```python
class GCSDownloadService:
    def parse_gcs_url(self, url: str) -> Tuple[str, str]  # Returns (bucket, file_path)
    def download_file(self, bucket_name: str, file_path: str) -> Tuple[bytes, str]  # Returns (content, content_type)
    def get_content_type(self, file_path: str) -> str
```

### 3. URL Parsing Logic
- Validate GCS URL format: `gs://bucket-name/path/to/file`
- Extract bucket name and file path components
- Handle edge cases (missing protocol, invalid format, etc.)

### 4. File Streaming
- Use StreamingResponse for efficient memory usage with large files
- Implement proper content-type detection based on file extension
- Set appropriate headers for browser download behavior

## Data Models

### Request Model
```python
class GCSDownloadRequest(BaseModel):
    file_url: str = Field(..., description="Google Cloud Storage file URL (gs://bucket/path)")
    
    @validator('file_url')
    def validate_gcs_url(cls, v):
        if not v.startswith('gs://'):
            raise ValueError('URL must start with gs://')
        if len(v.split('/')) < 4:  # gs://bucket/path minimum
            raise ValueError('Invalid GCS URL format')
        return v
```

### Response Models
```python
class GCSDownloadResponse(BaseModel):
    success: bool
    filename: str
    content_type: str
    size_bytes: Optional[int] = None

class GCSErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: str
```

## Error Handling

### Error Categories and HTTP Status Codes

1. **URL Validation Errors (400 Bad Request)**
   - Invalid GCS URL format
   - Missing or malformed bucket/path components

2. **Authentication Errors (401 Unauthorized)**
   - Invalid or expired GCS credentials
   - Insufficient permissions for bucket access

3. **File Not Found (404 Not Found)**
   - File does not exist in specified bucket
   - Bucket does not exist

4. **Server Errors (500 Internal Server Error)**
   - GCS service unavailable
   - Network connectivity issues
   - Unexpected parsing or processing errors

### Error Response Format
```python
{
    "success": false,
    "error": "Human-readable error message",
    "error_code": "VALIDATION_ERROR|AUTH_ERROR|NOT_FOUND|SERVER_ERROR"
}
```

## Testing Strategy

### Unit Tests
1. **URL Parsing Tests**
   - Valid GCS URLs with various path structures
   - Invalid URL formats and edge cases
   - Bucket and path extraction accuracy

2. **Service Layer Tests**
   - Mock GCS client responses for success/failure scenarios
   - Content-type detection for different file extensions
   - Error handling for various GCS exceptions

3. **Route Handler Tests**
   - Request validation with valid/invalid payloads
   - Response format verification
   - HTTP status code correctness

### Integration Tests
1. **End-to-End Download Flow**
   - Test with actual GCS bucket (test environment)
   - Verify file content integrity
   - Test with different file types and sizes

2. **Error Scenario Testing**
   - Non-existent files and buckets
   - Permission denied scenarios
   - Network timeout simulation

### Performance Considerations
- Memory usage testing with large files (streaming vs loading)
- Concurrent download request handling
- Response time benchmarks for different file sizes

## Security Considerations

1. **URL Validation**: Strict validation to prevent path traversal or injection attacks
2. **Credential Management**: Use existing secure credential handling from StorageService
3. **Access Control**: Ensure downloads respect GCS bucket permissions
4. **Rate Limiting**: Consider implementing rate limiting for download endpoints
5. **Logging**: Log download attempts without exposing sensitive URL parameters

## Implementation Notes

- Extend existing `StorageService` class rather than creating parallel GCS client
- Use `mimetypes` library for content-type detection
- Implement proper cleanup for streaming responses
- Follow existing application patterns for dependency injection
- Add comprehensive logging for debugging and monitoring