from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Existing models for presentation generation
class OutlineRequest(BaseModel):
    prompt: str
    numberOfCards: int
    language: str

class SlidesRequest(BaseModel):
    title: str
    outline: list[str]
    language: str
    tone: str

# New models for presentation management
class PresentationCreateRequest(BaseModel):
    title: str
    content: Dict[str, Any]
    theme: Optional[str] = "default"
    language: Optional[str] = "English"
    tone: Optional[str] = "Professional"
    user_id: int

class PresentationUpdateRequest(BaseModel):
    content: Optional[Dict[str, Any]] = None
    title: Optional[str] = None

class PresentationResponse(BaseModel):
    id: str
    title: str
    content: Dict[str, Any]
    theme: str
    language: str
    tone: str
    userId: str
    createdAt: str
    updatedAt: str
    isPublic: bool
    slug: Optional[str] = None

# Image generation models
class ImageGenerationRequest(BaseModel):
    prompt: str
    presentation_id: Optional[int] = None  # Added to link image to presentation
    user_email: Optional[str] = None
    size: Optional[str] = "1792x1024"  # Default to landscape for slides
    quality: Optional[str] = "hd"
    context: Optional[str] = None  # Additional context for better generation

class ImageGenerationResponse(BaseModel):
    success: bool
    url: Optional[str] = None
    prompt: Optional[str] = None
    model: Optional[str] = None
    size: Optional[str] = None
    quality: Optional[str] = None
    filename: Optional[str] = None
    error: Optional[str] = None

# Presentation Image models
class PresentationImageResponse(BaseModel):
    id: int
    presentation_id: int
    image_url: str
    prompt: str
    filename: Optional[str] = None
    model: str
    size: str
    created_at: datetime

class GeneratedImageResponse(BaseModel):
    id: str
    url: str
    prompt: str
    model: str
    size: Optional[str] = None
    quality: Optional[str] = None
    filename: Optional[str] = None
    userId: str
    createdAt: str

# User management models
class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    image: Optional[str] = None
    createdAt: str
    updatedAt: str

# New unified presentation generation model
class UnifiedPresentationRequest(BaseModel):
    # Required fields
    slides_count: int = Field(..., ge=3, le=20, description="Number of slides (3-20)")
    prompt: str = Field(..., min_length=10, description="Main presentation topic/prompt")
    
    # Optional fields
    color_theme: Optional[str] = Field("default", description="Presentation color theme")
    website_urls: Optional[List[str]] = Field([], description="Website URLs for context")
    context_sources: Optional[List[str]] = Field([], description="Additional context sources")
    industry_sector: Optional[str] = Field(None, description="Industry sector")
    one_line_pitch: Optional[str] = Field(None, description="One-line pitch")
    problem_solving: Optional[str] = Field(None, description="Problem you're solving")
    unique_solution: Optional[str] = Field(None, description="Your unique solution")
    target_audience: Optional[str] = Field(None, description="Target audience")
    business_model: Optional[str] = Field(None, description="Business model")
    revenue_plan: Optional[str] = Field(None, description="Revenue plan")
    competitors: Optional[str] = Field(None, description="Competitors analysis")
    vision: Optional[str] = Field(None, description="Company/project vision")
    
    # Presentation settings
    language: Optional[str] = Field("English", description="Presentation language")
    tone: Optional[str] = Field("Professional", description="Presentation tone")
    generate_images: Optional[bool] = Field(True, description="Generate AI images for slides")

class UnifiedPresentationResponse(BaseModel):
    success: bool
    presentation_xml: Optional[str] = None
    slides_count: int
    processing_time: float
    generated_images: List[Dict[str, Any]] = []
    context_sources_used: List[Dict[str, Any]] = []
    error: Optional[str] = None
    
    # Database information
    database_id: Optional[int] = None
    database_error: Optional[str] = None
    
    # Metadata
    prompt: str
    theme: str
    language: str
    tone: str