from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.short_video.models import (
    ShortVideoRequest,
    ShortVideoResponse,
    VideoGenerationResponse
)
from app.short_video.services.gemini_video_service import gemini_video_service
from app.short_video.crud import (
    create_short_video,
    get_short_video,
    get_user_short_videos,
    delete_short_video
)
from typing import List

router = APIRouter()

@router.post("/short-video/generate", response_model=ShortVideoResponse)
async def generate_short_video(request: ShortVideoRequest, db: Session = Depends(get_db)):
    """Generate a short video using AI and save to database"""
    try:
        print(f"🎬 Generating short video for user {request.user_id}")
        print(f"📝 Prompt: {request.prompt}")
        
        # Generate video using Gemini with Veo 3.0
        video_url = await gemini_video_service.generate_video(
            prompt=request.prompt
        )
        
        # Save to database with fixed values as requested
        video_record = create_short_video(
            db=db,
            user_id=request.user_id,
            prompt=request.prompt,
            video_url=video_url,
            aspect_ratio="16:9",
            duration=8,
            audio_generation=True,  # Boolean for database
            watermark=False,        # Boolean for database
            person_generation="allow-all"
        )
        
        return ShortVideoResponse(
            id=video_record.id,
            user_id=video_record.user_id,
            prompt=video_record.prompt,
            video_url=video_record.video_url,
            aspect_ratio=video_record.aspect_ratio,
            duration=video_record.duration,
            audio_generation=video_record.audio_generation,
            watermark=video_record.watermark,
            person_generation=video_record.person_generation,
            created_at=video_record.created_at,
            updated_at=video_record.updated_at
        )
        
    except Exception as e:
        print(f"❌ Video generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@router.get("/short-video/{video_id}", response_model=ShortVideoResponse)
async def get_short_video_endpoint(video_id: int, db: Session = Depends(get_db)):
    """Get a specific short video by ID"""
    video = get_short_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Short video not found")
    
    return ShortVideoResponse(
        id=video.id,
        user_id=video.user_id,
        prompt=video.prompt,
        video_url=video.video_url,
        aspect_ratio=video.aspect_ratio,
        duration=video.duration,
        audio_generation=video.audio_generation,
        watermark=video.watermark,
        person_generation=video.person_generation,
        created_at=video.created_at,
        updated_at=video.updated_at
    )

@router.get("/short-video/user/{user_id}", response_model=List[ShortVideoResponse])
async def get_user_short_videos_endpoint(user_id: int, db: Session = Depends(get_db)):
    """Get all short videos for a specific user"""
    videos = get_user_short_videos(db, user_id)
    return [
        ShortVideoResponse(
            id=v.id,
            user_id=v.user_id,
            prompt=v.prompt,
            video_url=v.video_url,
            aspect_ratio=v.aspect_ratio,
            duration=v.duration,
            audio_generation=v.audio_generation,
            watermark=v.watermark,
            person_generation=v.person_generation,
            created_at=v.created_at,
            updated_at=v.updated_at
        ) for v in videos
    ]

@router.delete("/short-video/{video_id}")
async def delete_short_video_endpoint(video_id: int, db: Session = Depends(get_db)):
    """Delete a short video"""
    success = delete_short_video(db, video_id)
    if not success:
        raise HTTPException(status_code=404, detail="Short video not found")
    return {"message": "Short video deleted successfully"}

@router.get("/short-video/status/check")
async def check_video_service_status():
    """Check if the video generation service is available"""
    try:
        # Test the actual Gemini video service connection
        service_healthy = gemini_video_service.test_connection()
        
        return {
            "status": "healthy" if service_healthy else "unhealthy",
            "service": "Gemini Video Generation with Veo 3.0",
            "model": "veo-3.0-generate-preview",
            "api": "google.genai",
            "fixed_settings": {
                "aspect_ratio": "16:9",
                "duration": "8 seconds",
                "audio_generation": "Yes",
                "watermark": "No",
                "person_generation": "allow-all"
            },
            "request_format": {
                "user_id": "integer",
                "prompt": "string (required)"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "Gemini Video Generation with Veo 3.0"
        }