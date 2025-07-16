import re

# Utility to slugify prompt for image filename
def slugify_prompt(prompt: str) -> str:
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', prompt.strip().lower())
    slug = slug.strip('_')
    return slug + '.png'
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.presentation.models import (
    OutlineRequest, 
    SlidesRequest, 
    PresentationCreateRequest,
    PresentationUpdateRequest,
    PresentationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    GeneratedImageResponse,
    UserResponse
)

from app.presentation.service.presentation_service import outline_chain, slides_chain
from app.presentation.service.enhanced_image_service import enhanced_image_service
from app.presentation.service.presentation_db_service import presentation_db_service
from typing import List

router = APIRouter()

# Helper function to map SQLAlchemy Presentation model to PresentationResponse
def to_presentation_response(presentation):
    import json
    content = presentation.content
    if isinstance(content, str):
        try:
            content = json.loads(content)
        except Exception:
            content = {"slides": []}
    return PresentationResponse(
        id=str(presentation.id),
        title=presentation.title,
        content=content,
        theme=presentation.theme,
        language=presentation.language,
        tone=presentation.tone,
        userId=str(presentation.user_id),
        createdAt=presentation.created_at.isoformat() if presentation.created_at else None,
        updatedAt=presentation.updated_at.isoformat() if presentation.updated_at else None,
        isPublic=presentation.is_public,
        slug=presentation.slug
    )

# Existing presentation generation endpoints
@router.post("/presentation/outline")
async def generate_outline(request: OutlineRequest):
    """Generate presentation outline using AI"""
    async def stream_response():
        async for chunk in outline_chain.astream({
            "prompt": request.prompt,
            "numberOfCards": request.numberOfCards,
            "language": request.language,
        }):
            yield chunk
    return StreamingResponse(stream_response(), media_type="text/plain")

@router.post("/presentation/generate")
async def generate_slides(request: SlidesRequest):
    """Generate presentation slides XML using AI"""
    async def stream_response():
        async for chunk in slides_chain.astream({
            "TITLE": request.title,
            "LANGUAGE": request.language,
            "TONE": request.tone,
            "OUTLINE_FORMATTED": "\n\n".join(request.outline),
            "TOTAL_SLIDES": len(request.outline),
        }):
            # Escape newlines and double quotes in the XML chunk
            if isinstance(chunk, str):
                chunk = chunk.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            yield chunk
    return StreamingResponse(stream_response(), media_type="application/xml")

# New image generation endpoint (replaces Together AI)
@router.post("/presentation/generate-image", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Generate image for presentations using DALL-E and store in GCS"""
    try:
        # Slugify the prompt for the image filename
        filename = slugify_prompt(request.prompt)
        bucket = "deck123"
        image_url = f"https://storage.googleapis.com/{bucket}/{filename}"

        # Generate image using DALL-E service and upload with the slugified filename
        # The enhanced_image_service should accept a filename override (add this if not present)
        generated_url = await enhanced_image_service.generate_presentation_image(
            prompt=request.prompt,
            model="dall-e-3",
            size=request.size or "1024x1024",
            filename=filename
        )
        # Use the actual generated URL if the service returns it, else use the constructed one
        final_url = generated_url or image_url


        return ImageGenerationResponse(
            success=True,
            url=final_url,
            prompt=request.prompt,
            model="dall-e-3",
            size=request.size or "1024x1024"
        )

    except Exception as e:
        return ImageGenerationResponse(
            success=False,
            error=str(e)
        )

# Database CRUD operations for presentations
@router.post("/presentation/create", response_model=PresentationResponse)
async def create_presentation(request: PresentationCreateRequest):
    """Create a new presentation in database"""
    import json
    try:
        content = request.content
        if isinstance(content, str):
            # Always use json.dumps to ensure valid JSON string escaping
            # Remove surrounding quotes after dumps to store as plain string
            content = json.dumps(content)[1:-1]
        presentation = await presentation_db_service.create_presentation(
            title=request.title,
            content=content,
            user_id=request.user_id,  # use user_id here
            theme=request.theme,
            language=request.language,
            tone=request.tone
        )
        return to_presentation_response(presentation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/presentation/{presentation_id}", response_model=PresentationResponse)
async def get_presentation(presentation_id: str):
    """Get presentation by ID"""
    presentation = await presentation_db_service.get_presentation(presentation_id)
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return to_presentation_response(presentation)

@router.put("/presentation/{presentation_id}", response_model=PresentationResponse)
async def update_presentation(presentation_id: str, request: PresentationUpdateRequest):
    """Update presentation content"""
    try:
        presentation = await presentation_db_service.update_presentation(
            presentation_id=presentation_id,
            content=request.content,
            title=request.title
        )
        return to_presentation_response(presentation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/presentation/user/{user_email}", response_model=List[PresentationResponse])
async def get_user_presentations(user_email: str):
    """Get all presentations for a user"""
    presentations = await presentation_db_service.get_user_presentations(user_email)
    return [PresentationResponse(**p) for p in presentations]

@router.delete("/presentation/{presentation_id}")
async def delete_presentation(presentation_id: str):
    """Delete presentation"""
    success = await presentation_db_service.delete_presentation(presentation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return {"message": "Presentation deleted successfully"}

# Image management endpoints
@router.get("/presentation/images/{user_email}", response_model=List[GeneratedImageResponse])
async def get_user_images(user_email: str, limit: int = 50):
    """Get generated images for a user"""
    images = await presentation_db_service.get_user_images(user_email, limit)
    return [GeneratedImageResponse(**img) for img in images]

@router.get("/presentation/image-info")
async def get_image_info(url: str):
    """Get image metadata by URL"""
    image = await presentation_db_service.get_image_by_url(url)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return GeneratedImageResponse(**image)