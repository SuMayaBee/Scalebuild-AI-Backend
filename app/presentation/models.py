from pydantic import BaseModel
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