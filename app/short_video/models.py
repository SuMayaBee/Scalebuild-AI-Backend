from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShortVideoRequest(BaseModel):
    user_id: int
    prompt: str

class ShortVideoRequestFull(BaseModel):
    """Full request model for backward compatibility"""
    user_id: int
    prompt: str
    aspect_ratio: Optional[str] = "16:9"
    duration: Optional[str] = "8"
    audio_generation: Optional[bool] = True
    watermark: Optional[bool] = True
    person_generation: Optional[str] = "allow_all"

class ShortVideoResponse(BaseModel):
    id: int
    user_id: int
    prompt: str
    video_url: str
    aspect_ratio: str
    duration: str
    audio_generation: bool
    watermark: bool
    person_generation: str
    created_at: datetime
    updated_at: datetime

class VideoGenerationResponse(BaseModel):
    success: bool
    video_url: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None