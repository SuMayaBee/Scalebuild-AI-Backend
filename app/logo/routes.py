from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.logo import (
    LogoRequest,
    LogoDesignResponse,
    LogoDescriptionResponse,
    LogoImageResponse,
    CompleteLogoResponse,
    ColorPalette
)
from services.logo_service import (
    generate_logo_design, 
    generate_logo_description,
    generate_logo_image,
    generate_complete_logo,
    COLOR_PALETTES, 
    LOGO_STYLES
)
import json
from typing import List

router = APIRouter()

@router.post("/logo/design", response_model=LogoDesignResponse)
async def create_logo_design(request: LogoRequest):
    """Generate a comprehensive logo design specification using GPT-4o"""
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

@router.post("/logo/description", response_model=LogoDescriptionResponse)
async def create_logo_description(request: LogoRequest):
    """Generate a detailed visual description of the logo using GPT-4o"""
    try:
        result = await generate_logo_description(
            logo_title=request.logo_title,
            logo_vision=request.logo_vision,
            color_palette_name=request.color_palette_name,
            logo_style=request.logo_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logo/design-stream")
async def create_logo_design_stream(request: LogoRequest):
    """Generate a logo design specification with streaming response"""
    async def stream_logo_design():
        try:
            yield "data: " + json.dumps({
                "status": "analyzing", 
                "message": f"Analyzing design requirements for '{request.logo_title}'..."
            }) + "\n\n"
            
            result = await generate_logo_design(
                logo_title=request.logo_title,
                logo_vision=request.logo_vision,
                color_palette_name=request.color_palette_name,
                logo_style=request.logo_style
            )
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_logo_design(), media_type="text/plain")

@router.post("/logo/description-stream")
async def create_logo_description_stream(request: LogoRequest):
    """Generate a logo description with streaming response"""
    async def stream_logo_description():
        try:
            yield "data: " + json.dumps({
                "status": "creating", 
                "message": f"Creating detailed description for '{request.logo_title}'..."
            }) + "\n\n"
            
            result = await generate_logo_description(
                logo_title=request.logo_title,
                logo_vision=request.logo_vision,
                color_palette_name=request.color_palette_name,
                logo_style=request.logo_style
            )
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_logo_description(), media_type="text/plain")

@router.post("/logo/image", response_model=LogoImageResponse)
async def create_logo_image(request: LogoRequest):
    """Generate a logo image using GPT-4o, save to Google Cloud Storage"""
    try:
        result = await generate_logo_image(
            request.logo_title,
            request.logo_vision, 
            request.color_palette_name,
            request.logo_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logo/complete", response_model=CompleteLogoResponse)
async def create_complete_logo(request: LogoRequest):
    """Generate both design specification and logo image"""
    try:
        result = await generate_complete_logo(
            request.logo_title,
            request.logo_vision, 
            request.color_palette_name,
            request.logo_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logo/image-stream")
async def create_logo_image_stream(request: LogoRequest):
    """Generate logo image with streaming response for real-time updates"""
    async def stream_logo_generation():
        try:
            yield "data: " + json.dumps({"status": "generating_prompt", "message": "Analyzing your requirements with GPT-4o..."}) + "\n\n"
            
            yield "data: " + json.dumps({"status": "generating_image", "message": "Creating logo with GPT-4o..."}) + "\n\n"
            
            result = await generate_logo_image(
                request.logo_title,
                request.logo_vision, 
                request.color_palette_name,
                request.logo_style
            )
            
            yield "data: " + json.dumps({"status": "uploading", "message": "Uploading to Google Cloud Storage..."}) + "\n\n"
            
            yield "data: " + json.dumps({
                "status": "complete", 
                "data": result
            }) + "\n\n"
            
        except Exception as e:
            yield "data: " + json.dumps({
                "status": "error", 
                "message": str(e)
            }) + "\n\n"
    
    return StreamingResponse(stream_logo_generation(), media_type="text/plain")

@router.get("/logo/color-palettes", response_model=List[ColorPalette])
async def get_color_palettes():
    """Get all available color palettes"""
    palettes = []
    for name, colors in COLOR_PALETTES.items():
        palettes.append({
            "name": name,
            "colors": colors
        })
    return palettes

@router.get("/logo/styles")
async def get_logo_styles():
    """Get all available logo styles"""
    return {"logo_styles": LOGO_STYLES}
