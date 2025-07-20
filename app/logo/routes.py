from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.logo.models.logo import (
    LogoRequest,
    LogoDesignResponse,
    LogoDescriptionResponse,
    LogoImageResponse,
    CompleteLogoResponse,
    ColorPalette,
    LogoResponse,
    RemoveBackgroundRequest,
    RemoveBackgroundResponse
)
from app.logo.service.logo_service import (
    generate_logo_design, 
    generate_logo_description,
    generate_logo_image,
    generate_complete_logo,
    COLOR_PALETTES, 
    LOGO_STYLES
)
from app.logo.service.background_removal_service import remove_background_from_url
from app.logo.service.crud import (
    create_logo,
    get_logo,
    get_user_logos,
    update_logo_remove_bg_url,
    delete_logo
)
import json
from typing import List

router = APIRouter()

@router.post("/logo/design", response_model=LogoResponse)
async def create_logo_design(request: LogoRequest, db: Session = Depends(get_db)):
    """Generate a logo design, save to database and return logo with image URL"""
    try:
        # Generate logo image using the service
        image_result = await generate_logo_image(
            logo_title=request.logo_title,
            logo_vision=request.logo_vision,
            color_palette_name=request.color_palette_name,
            logo_style=request.logo_style
        )
        
        # Generate design specification for content
        design_result = await generate_logo_design(
            logo_title=request.logo_title,
            logo_vision=request.logo_vision,
            color_palette_name=request.color_palette_name,
            logo_style=request.logo_style
        )
        
        # Prepare content to store in database
        content = {
            "design_specification": design_result.get("design_specification"),
            "generation_type": design_result.get("generation_type"),
            "enhanced_prompt": image_result.get("enhanced_prompt"),
            "image_model": image_result.get("image_model")
        }
        
        # Save to database
        logo = create_logo(
            db=db,
            user_id=request.user_id,
            logo_image_url=image_result["logo_image_url"],
            logo_title=request.logo_title,
            logo_vision=request.logo_vision,
            color_palette_name=request.color_palette_name,
            logo_style=request.logo_style,
            content=content
        )
        
        return LogoResponse(
            id=logo.id,
            user_id=logo.user_id,
            logo_image_url=logo.logo_image_url,
            remove_bg_logo_image_url=logo.remove_bg_logo_image_url,
            content=logo.content,
            logo_title=logo.logo_title,
            logo_vision=logo.logo_vision,
            color_palette_name=logo.color_palette_name,
            logo_style=logo.logo_style,
            created_at=logo.created_at,
            updated_at=logo.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logo/remove_bg", response_model=RemoveBackgroundResponse)
async def remove_logo_background(request: RemoveBackgroundRequest, db: Session = Depends(get_db)):
    """Remove background from a logo and update the database"""
    try:
        # Get the logo from database
        logo = get_logo(db, request.logo_id)
        if not logo:
            raise HTTPException(status_code=404, detail="Logo not found")
        
        # Remove background from the logo image
        bg_removal_result = await remove_background_from_url(logo.logo_image_url)
        
        # Update the logo with the new background-removed URL
        updated_logo = update_logo_remove_bg_url(
            db=db,
            logo_id=request.logo_id,
            remove_bg_url=bg_removal_result["new_image_url"]
        )
        
        return RemoveBackgroundResponse(
            success=True,
            logo_id=request.logo_id,
            remove_bg_logo_image_url=bg_removal_result["new_image_url"]
        )
        
    except Exception as e:
        return RemoveBackgroundResponse(
            success=False,
            logo_id=request.logo_id,
            error=str(e)
        )

@router.get("/logo/{logo_id}", response_model=LogoResponse)
async def get_logo_by_id(logo_id: int, db: Session = Depends(get_db)):
    """Get a specific logo by ID"""
    logo = get_logo(db, logo_id)
    if not logo:
        raise HTTPException(status_code=404, detail="Logo not found")
    
    return LogoResponse(
        id=logo.id,
        user_id=logo.user_id,
        logo_image_url=logo.logo_image_url,
        remove_bg_logo_image_url=logo.remove_bg_logo_image_url,
        content=logo.content,
        logo_title=logo.logo_title,
        logo_vision=logo.logo_vision,
        color_palette_name=logo.color_palette_name,
        logo_style=logo.logo_style,
        created_at=logo.created_at,
        updated_at=logo.updated_at
    )

@router.get("/logo/user/{user_id}", response_model=List[LogoResponse])
async def get_user_logos_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all logos for a specific user"""
    logos = get_user_logos(db, user_id)
    return [
        LogoResponse(
            id=logo.id,
            user_id=logo.user_id,
            logo_image_url=logo.logo_image_url,
            remove_bg_logo_image_url=logo.remove_bg_logo_image_url,
            content=logo.content,
            logo_title=logo.logo_title,
            logo_vision=logo.logo_vision,
            color_palette_name=logo.color_palette_name,
            logo_style=logo.logo_style,
            created_at=logo.created_at,
            updated_at=logo.updated_at
        ) for logo in logos
    ]

@router.delete("/logo/{logo_id}")
async def delete_logo_endpoint(logo_id: int, db: Session = Depends(get_db)):
    """Delete a logo"""
    success = delete_logo(db, logo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Logo not found")
    return {"message": "Logo deleted successfully"}

# Keep the original design-only endpoint for backward compatibility
@router.post("/logo/design-only", response_model=LogoDesignResponse)
async def create_logo_design_only(request: LogoRequest):
    """Generate only a logo design specification (no database save)"""
    try:
        result = await generate_logo_design(
            logo_title=request.logo_title,
            logo_vision=request.logo_vision,
            color_palette_name=request.color_palette_name,
            logo_style=request.logo_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
