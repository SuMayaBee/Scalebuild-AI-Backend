"""
Enhanced Presentation Routes with better error handling and new features
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.auth.db_models import User
from app.presentation.models import (
    OutlineRequest, 
    SlidesRequest, 
    ImageGenerationRequest,
    ImageGenerationResponse,
    PresentationCreateRequest,
    PresentationResponse
)
from app.presentation.service.presentation_service import outline_chain, slides_chain
from app.presentation.service.improved_presentation_service import (
    improved_presentation_service,
    PresentationServiceError,
    PresentationNotFoundError,
    ImageGenerationError
)
from typing import List, Optional

router = APIRouter()

# Health check endpoint
@router.get("/health")
async def health_check():
    """Check health of all presentation services"""
    try:
        health_status = await improved_presentation_service.health_check()
        
        if health_status["overall"]:
            return {"status": "healthy", "services": health_status}
        else:
            raise HTTPException(
                status_code=503, 
                detail={"status": "unhealthy", "services": health_status}
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Existing AI generation endpoints (unchanged)
@router.post("/outline")
async def generate_outline(request: OutlineRequest):
    """Generate presentation outline using AI"""
    try:
        async def stream_response():
            async for chunk in outline_chain.astream({
                "prompt": request.prompt,
                "numberOfCards": request.numberOfCards,
                "language": request.language,
            }):
                yield chunk
        return StreamingResponse(stream_response(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outline generation failed: {str(e)}")

@router.post("/generate")
async def generate_slides(request: SlidesRequest):
    """Generate presentation slides XML using AI"""
    try:
        async def stream_response():
            async for chunk in slides_chain.astream({
                "TITLE": request.title,
                "LANGUAGE": request.language,
                "TONE": request.tone,
                "OUTLINE_FORMATTED": "\n\n".join(request.outline),
                "TOTAL_SLIDES": len(request.outline),
            }):
                if isinstance(chunk, str):
                    chunk = chunk.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                yield chunk
        return StreamingResponse(stream_response(), media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Slides generation failed: {str(e)}")

# Enhanced image generation endpoint
@router.post("/generate-image-enhanced", response_model=ImageGenerationResponse)
async def generate_image_enhanced(
    request: ImageGenerationRequest,
    prefer_ai: bool = Query(True, description="Prefer AI generation over search"),
    current_user: User = Depends(get_current_user)
):
    """Enhanced image generation with fallback strategy and user authentication"""
    try:
        result = await improved_presentation_service.generate_image_with_fallback(
            prompt=request.prompt,
            presentation_id=request.presentation_id,
            prefer_ai=prefer_ai,
            size=request.size or "1024x1024"
        )
        
        if result["success"]:
            return ImageGenerationResponse(
                success=True,
                url=result["url"],
                prompt=request.prompt,
                model=result["model"],
                size=result.get("size"),
                filename=result.get("filename")
            )
        else:
            return ImageGenerationResponse(
                success=False,
                error=result.get("error", "Image generation failed")
            )
            
    except ImageGenerationError as e:
        return ImageGenerationResponse(
            success=False,
            error=str(e)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation error: {str(e)}")

# Enhanced presentation management
@router.post("/create-enhanced", response_model=PresentationResponse)
async def create_presentation_enhanced(
    request: PresentationCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """Create presentation with enhanced validation and error handling"""
    try:
        # Use current user's ID instead of request user_id for security
        presentation = await improved_presentation_service.create_presentation_with_validation(
            title=request.title,
            content=request.content,
            user_id=current_user.id,  # Use authenticated user's ID
            theme=request.theme,
            language=request.language,
            tone=request.tone
        )
        
        return PresentationResponse(
            id=str(presentation["id"]),
            title=presentation["title"],
            content=presentation["content"],
            theme=presentation["theme"],
            language=presentation["language"],
            tone=presentation["tone"],
            userId=str(presentation["user_id"]),
            createdAt=presentation["created_at"],
            updatedAt=presentation["updated_at"],
            isPublic=presentation.get("is_public", False),
            slug=presentation.get("slug")
        )
        
    except PresentationServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Presentation creation failed: {str(e)}")

@router.get("/{presentation_id}/enhanced", response_model=PresentationResponse)
async def get_presentation_enhanced(
    presentation_id: int,
    include_images: bool = Query(False, description="Include associated images"),
    current_user: User = Depends(get_current_user)
):
    """Get presentation with optional image inclusion"""
    try:
        if include_images:
            presentation = await improved_presentation_service.get_presentation_with_images(presentation_id)
        else:
            presentation = await improved_presentation_service.get_presentation_with_images(presentation_id)
            # Remove images from response if not requested
            presentation.pop("images", None)
        
        # Check if user has access to this presentation
        if presentation["user_id"] != current_user.id:
            # Check if presentation is public
            if not presentation.get("is_public", False):
                raise HTTPException(status_code=403, detail="Access denied to this presentation")
        
        return PresentationResponse(
            id=str(presentation["id"]),
            title=presentation["title"],
            content=presentation["content"],
            theme=presentation["theme"],
            language=presentation["language"],
            tone=presentation["tone"],
            userId=str(presentation["user_id"]),
            createdAt=presentation["created_at"],
            updatedAt=presentation["updated_at"],
            isPublic=presentation.get("is_public", False),
            slug=presentation.get("slug")
        )
        
    except PresentationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PresentationServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve presentation: {str(e)}")

@router.get("/my-presentations/enhanced")
async def get_my_presentations_with_stats(
    current_user: User = Depends(get_current_user)
):
    """Get current user's presentations with statistics"""
    try:
        result = await improved_presentation_service.get_user_presentations_with_stats(current_user.id)
        
        return {
            "presentations": result["presentations"],
            "statistics": result["statistics"],
            "user": {
                "id": current_user.id,
                "email": current_user.email,
                "name": current_user.name
            }
        }
        
    except PresentationServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve presentations: {str(e)}")

# Batch operations
@router.post("/batch-generate-images")
async def batch_generate_images(
    prompts: List[str],
    presentation_id: Optional[int] = None,
    prefer_ai: bool = Query(True, description="Prefer AI generation over search"),
    current_user: User = Depends(get_current_user)
):
    """Generate multiple images in batch for better performance"""
    try:
        if len(prompts) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 prompts allowed per batch")
        
        results = []
        for prompt in prompts:
            try:
                result = await improved_presentation_service.generate_image_with_fallback(
                    prompt=prompt,
                    presentation_id=presentation_id,
                    prefer_ai=prefer_ai
                )
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "prompt": prompt,
                    "error": str(e)
                })
        
        return {
            "results": results,
            "summary": {
                "total": len(prompts),
                "successful": len([r for r in results if r.get("success")]),
                "failed": len([r for r in results if not r.get("success")])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch image generation failed: {str(e)}")

# Analytics endpoint
@router.get("/analytics/usage")
async def get_usage_analytics(
    current_user: User = Depends(get_current_user)
):
    """Get usage analytics for the current user"""
    try:
        result = await improved_presentation_service.get_user_presentations_with_stats(current_user.id)
        
        # Additional analytics
        analytics = {
            "user_id": current_user.id,
            "total_presentations": result["statistics"]["total_presentations"],
            "total_images": result["statistics"]["total_images"],
            "theme_preferences": result["statistics"]["theme_distribution"],
            "language_preferences": result["statistics"]["language_distribution"],
            "average_images_per_presentation": (
                result["statistics"]["total_images"] / result["statistics"]["total_presentations"]
                if result["statistics"]["total_presentations"] > 0 else 0
            ),
            "most_used_theme": max(
                result["statistics"]["theme_distribution"].items(),
                key=lambda x: x[1]
            )[0] if result["statistics"]["theme_distribution"] else None,
            "most_used_language": max(
                result["statistics"]["language_distribution"].items(),
                key=lambda x: x[1]
            )[0] if result["statistics"]["language_distribution"] else None
        }
        
        return analytics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics retrieval failed: {str(e)}")

# Configuration endpoint
@router.get("/config")
async def get_presentation_config():
    """Get available configuration options"""
    return {
        "themes": ["default", "modern", "classic", "minimal", "corporate"],
        "languages": ["English", "Spanish", "French", "German", "Chinese", "Japanese"],
        "tones": ["Professional", "Casual", "Academic", "Creative", "Technical"],
        "image_sizes": ["1024x1024", "1792x1024", "1024x1792"],
        "max_slides_per_presentation": 50,
        "max_images_per_batch": 10,
        "supported_image_models": ["dall-e-3", "dall-e-2", "google_search"]
    }