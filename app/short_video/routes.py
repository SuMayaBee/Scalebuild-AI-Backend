from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.short_video.models import (
    ShortVideoRequest,
    ShortVideoResponse,
    VideoGenerationResponse
)
from app.short_video.services.video_generation_service import video_generation_service
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
        # Generate video using Veo 3.0
        video_url = await video_generation_service.generate_video(
            prompt=request.prompt,
            aspect_ratio=request.aspect_ratio,
            duration=request.duration,
            audio_generation=request.audio_generation,
            watermark=request.watermark,
            person_generation=request.person_generation
        )
        
        # Save to database
        video_record = create_short_video(
            db=db,
            user_id=request.user_id,
            prompt=request.prompt,
            video_url=video_url,
            aspect_ratio=request.aspect_ratio,
            duration=request.duration,
            audio_generation=request.audio_generation,
            watermark=request.watermark,
            person_generation=request.person_generation
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
        # Simple health check
        return {
            "status": "healthy",
            "service": "Veo 3.0 Video Generation",
            "model": "veo-3.0-generate-preview",
            "available_options": {
                "aspect_ratios": ["16:9", "9:16", "1:1"],
                "durations": ["4", "8"],
                "person_generation": ["allow_all", "allow_none", "allow_some"]
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }