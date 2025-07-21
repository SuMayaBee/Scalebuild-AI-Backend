"""
Google Cloud Storage Routes
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import io
from .models import GCSDownloadRequest, GCSDownloadResponse, GCSErrorResponse
from .services.download_service import GCSDownloadService

router = APIRouter()

@router.post("/download", response_model=GCSDownloadResponse)
async def download_gcs_file(request: GCSDownloadRequest):
    """
    Download a file from Google Cloud Storage and return it as a streaming response.
    
    Args:
        request: GCSDownloadRequest containing the GCS file URL
        
    Returns:
        StreamingResponse with the file content
    """
    try:
        download_service = GCSDownloadService()
        
        # Download the file
        file_content, filename, content_type, size_bytes = download_service.download_file(request.file_url)
        
        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(file_content.read()),
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(size_bytes)
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/file-info")
async def get_gcs_file_info(request: GCSDownloadRequest):
    """
    Get information about a file in Google Cloud Storage without downloading it.
    
    Args:
        request: GCSDownloadRequest containing the GCS file URL
        
    Returns:
        File information including size, content type, etc.
    """
    try:
        download_service = GCSDownloadService()
        
        # Get file information
        file_info = download_service.get_file_info(request.file_url)
        
        return {
            "success": True,
            "file_info": file_info
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for GCS service."""
    return {"status": "healthy", "service": "gcs-download"}