from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ColorPalette(BaseModel):
    name: str
    colors: List[str]

class LogoRequest(BaseModel):
    logo_title: str
    logo_vision: str  # Describe your logo vision
    color_palette_name: str  # Name from the predefined color palettes
    logo_style: str  # Cartoon Logo, App Logo, Modern Mascot Logos, etc.
    user_id: int  # Added user_id to link logo to user

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

# Database response models
class LogoResponse(BaseModel):
    id: int
    user_id: int
    logo_image_url: str
    remove_bg_logo_image_url: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    logo_title: str
    logo_vision: Optional[str] = None
    color_palette_name: Optional[str] = None
    logo_style: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class RemoveBackgroundRequest(BaseModel):
    logo_id: int

class RemoveBackgroundResponse(BaseModel):
    success: bool
    logo_id: int
    remove_bg_logo_image_url: Optional[str] = None
    error: Optional[str] = None
