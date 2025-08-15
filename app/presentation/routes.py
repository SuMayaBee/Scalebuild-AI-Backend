import re

# Utility to slugify prompt for image filename (preserving original case)
def slugify_prompt(prompt: str) -> str:
    # Replace non-alphanumeric characters with underscores, preserving original case
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', prompt.strip())
    slug = slug.strip('_')
    return slug + '.png'
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.presentation.models import (
    OutlineRequest, 
    SlidesRequest, 
    PresentationCreateRequest,
    PresentationUpdateRequest,
    PresentationResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    GeneratedImageResponse,
    UserResponse,
    PresentationImageResponse,
    UnifiedPresentationRequest,
    UnifiedPresentationResponse
)

from app.presentation.service.presentation_service import outline_chain, slides_chain
from app.presentation.service.enhanced_image_service import enhanced_image_service
from app.presentation.service.presentation_db_service import presentation_db_service
from app.presentation.service.unified_presentation_service import unified_presentation_service
from app.presentation.service.crud import create_presentation_image, get_presentation_images
from app.presentation.db_models import Presentation
from app.core.security import get_current_user
from app.auth.db_models import User
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

# NEW UNIFIED PRESENTATION ENDPOINT WITH FILE UPLOADS
@router.post("/presentation/generate-unified", response_model=UnifiedPresentationResponse)
async def generate_unified_presentation(
    request: Request,
    # Required fields
    slides_count: int = Form(..., ge=3, le=20, description="Number of slides (3-20)"),
    prompt: str = Form(..., min_length=10, description="Main presentation topic/prompt"),
    
    # Optional fields
    color_theme: Optional[str] = Form("default", description="Presentation color theme"),
    website_urls: Optional[str] = Form(None, description="Comma-separated website URLs"),
    industry_sector: Optional[str] = Form(None, description="Industry sector"),
    one_line_pitch: Optional[str] = Form(None, description="One-line pitch"),
    problem_solving: Optional[str] = Form(None, description="Problem you're solving"),
    unique_solution: Optional[str] = Form(None, description="Your unique solution"),
    target_audience: Optional[str] = Form(None, description="Target audience"),
    business_model: Optional[str] = Form(None, description="Business model"),
    revenue_plan: Optional[str] = Form(None, description="Revenue plan"),
    competitors: Optional[str] = Form(None, description="Competitors analysis"),
    vision: Optional[str] = Form(None, description="Company/project vision"),
    language: Optional[str] = Form("English", description="Presentation language"),
    tone: Optional[str] = Form("Professional", description="Presentation tone"),
    generate_images: Optional[bool] = Form(True, description="Generate AI images for slides"),
    
    # User identification
    user_id: int = Form(..., description="User ID for presentation ownership")
):
    """
    Generate complete presentation with RAG context integration
    
    This endpoint combines outline and slide generation with RAG integration for:
    - Website URLs processing
    - Document file uploads for context
    - Business information incorporation
    - AI image generation
    """
    try:
        print(f"🎯 Starting unified presentation generation for user {user_id}")
        
        # Process website URLs
        website_url_list = []
        if website_urls:
            website_url_list = [url.strip() for url in website_urls.split(',') if url.strip()]
        
        # Process uploaded context files (handle manually from request)
        context_documents = []
        try:
            # Get form data from request
            form_data = await request.form()
            context_files = form_data.getlist("context_files")
            
            if context_files and len(context_files) > 0:
                # Filter out empty strings and only process actual UploadFile objects
                actual_files = [f for f in context_files if hasattr(f, 'filename') and f.filename]
                
                if actual_files:
                    print(f"📄 Processing {len(actual_files)} uploaded context files...")
                    
                    for file in actual_files:
                        try:
                            # Read file content
                            file_content = await file.read()
                            
                            # Process document with RAG service
                            from Rag.services.document_processor import document_processor
                            
                            # Extract text from uploaded file
                            extraction_result = document_processor.extract_text_from_file(
                                file_content=file_content,
                                filename=file.filename
                            )
                            
                            if extraction_result["text"].strip():
                                context_documents.append({
                                    "filename": file.filename,
                                    "content": extraction_result["text"],
                                    "metadata": extraction_result["metadata"]
                                })
                                print(f"✅ Processed context file: {file.filename}")
                            else:
                                print(f"⚠️ No content extracted from: {file.filename}")
                                
                        except Exception as e:
                            print(f"❌ Error processing file {file.filename}: {e}")
                            continue
                else:
                    print("📄 No valid files found in context_files")
            else:
                print("📄 No context files provided")
                
        except Exception as e:
            print(f"⚠️ Error processing form data: {e}")
            # Continue without files if there's an error
        
        # Generate presentation with RAG context (no image generation)
        result = await unified_presentation_service.generate_presentation_with_context(
            user_id=user_id,  # Use provided user ID from request
            slides_count=slides_count,
            prompt=prompt,
            color_theme=color_theme or "default",
            website_urls=website_url_list,
            context_documents=context_documents,  # Pass processed documents instead of text sources
            industry_sector=industry_sector,
            one_line_pitch=one_line_pitch,
            problem_solving=problem_solving,
            unique_solution=unique_solution,
            target_audience=target_audience,
            business_model=business_model,
            revenue_plan=revenue_plan,
            competitors=competitors,
            vision=vision,
            language=language or "English",
            tone=tone or "Professional",
            generate_images=False  # Always disable image generation
        )
        
        # Save presentation to database if generation was successful
        if result["success"] and result["presentation_xml"]:
            try:
                print("💾 Saving presentation to database...")
                
                # Create presentation content structure
                presentation_content = {
                    "slides": result["presentation_xml"],
                    "context_sources": result["context_sources_used"],
                    "business_context": {
                        "industry_sector": industry_sector,
                        "one_line_pitch": one_line_pitch,
                        "problem_solving": problem_solving,
                        "unique_solution": unique_solution,
                        "target_audience": target_audience,
                        "business_model": business_model,
                        "revenue_plan": revenue_plan,
                        "competitors": competitors,
                        "vision": vision
                    },
                    "generation_metadata": {
                        "slides_count": slides_count,
                        "processing_time": result["processing_time"],
                        "website_urls": website_url_list,
                        "context_files": [doc.get("filename") for doc in context_documents]
                    }
                }
                
                # Save to database using presentation service
                saved_presentation = await presentation_db_service.create_presentation(
                    title=prompt,
                    content=presentation_content,
                    user_id=user_id,  # Use provided user ID from request
                    theme=color_theme or "default",
                    language=language or "English",
                    tone=tone or "Professional"
                )
                
                # Add presentation ID to result (both fields for clarity and backward compatibility)
                result["presentation_id"] = saved_presentation.id
                result["database_id"] = saved_presentation.id
                print(f"✅ Presentation saved to database with ID: {saved_presentation.id}")
                
            except Exception as db_error:
                print(f"⚠️ Error saving to database: {db_error}")
                # Don't fail the request if database save fails
                result["database_error"] = str(db_error)
        
        # Always return empty images array
        result["generated_images"] = []
        
        return UnifiedPresentationResponse(**result)
        
    except Exception as e:
        print(f"❌ Error in unified presentation generation: {e}")
        return UnifiedPresentationResponse(
            success=False,
            presentation_xml=None,
            slides_count=slides_count,
            processing_time=0.0,
            generated_images=[],
            context_sources_used=[],
            error=str(e),
            prompt=prompt,
            theme=color_theme or "default",
            language=language or "English",
            tone=tone or "Professional"
        )

# Existing presentation generation endpoints (kept for backward compatibility)
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
async def generate_image(request: ImageGenerationRequest, db: Session = Depends(get_db)):
    """Generate image for presentations using DALL-E and store in GCS and database"""
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

        # Save image to database if presentation_id is provided
        if request.presentation_id:
            create_presentation_image(
                db=db,
                presentation_id=request.presentation_id,
                image_url=final_url,
                prompt=request.prompt,
                filename=filename,
                model="dall-e-3",
                size=request.size or "1024x1024"
            )

        return ImageGenerationResponse(
            success=True,
            url=final_url,
            prompt=request.prompt,
            model="dall-e-3",
            size=request.size or "1024x1024",
            filename=filename
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
    """Get all presentations for a user by email"""
    presentations = await presentation_db_service.get_user_presentations(user_email)
    return [PresentationResponse(**p) for p in presentations]

@router.get("/presentation/user-id/{user_id}", response_model=List[PresentationResponse])
async def get_user_presentations_by_id(user_id: int):
    """Get all presentations for a user by user ID"""
    presentations = await presentation_db_service.get_user_presentations_by_id(user_id)
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

# Presentation Image endpoints
@router.get("/presentation/{presentation_id}/images", response_model=List[PresentationImageResponse])
async def get_presentation_images_endpoint(presentation_id: int, db: Session = Depends(get_db)):
    """Get all images for a specific presentation"""
    try:
        images = get_presentation_images(db, presentation_id)
        return [
            PresentationImageResponse(
                id=img.id,
                presentation_id=img.presentation_id,
                image_url=img.image_url,
                prompt=img.prompt,
                filename=img.filename,
                model=img.model,
                size=img.size,
                created_at=img.created_at
            ) for img in images
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")