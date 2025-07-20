from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ColorPalette(BaseModel):
    name: str
    colors: List[str]

class LogoRequest(BaseModel):
    logo_title: str
    logo_vision: str  # Describe your logo vision
    color_palette_name: str  # Name from the predefined color palettes
    logo_style: str  # Cartoon Logo, App Logo, Modern Mascot Logos, etc.

class LogoDesignResponse(BaseModel):
    design_specification: Dict[str, Any]
    raw_specification: str
    logo_title: str
    generation_type: str

class LogoDescriptionResponse(BaseModel):
    logo_description: str
    logo_title: str
    parameters: Dict[str, str]

class LogoImageResponse(BaseModel):
    logo_image_url: str
    logo_title: str
    enhanced_prompt: str
    original_request: Dict[str, str]
    image_model: str

class CompleteLogoResponse(BaseModel):
    design_specification: Dict[str, Any]
    raw_specification: str
    logo_title: str
    generation_type: str
    logo_image_url: str
    enhanced_prompt: str
    image_model: str
