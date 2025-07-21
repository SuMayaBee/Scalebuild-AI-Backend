from sqlalchemy.orm import Session
from app.short_video.db_models import ShortVideo
from typing import Optional

def create_short_video(
    db: Session,
    user_id: int,
    prompt: str,
    video_url: str,
    aspect_ratio: str = "16:9",
    duration: str = "8",
    audio_generation: bool = True,
    watermark: bool = True,
    person_generation: str = "allow_all"
):
    """Create a new short video record"""
    video = ShortVideo(
        user_id=user_id,
        prompt=prompt,
        video_url=video_url,
        aspect_ratio=aspect_ratio,
        duration=duration,
        audio_generation=audio_generation,
        watermark=watermark,
        person_generation=person_generation
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    return video

def get_short_video(db: Session, video_id: int):
    """Get a specific short video by ID"""
    return db.query(ShortVideo).filter(ShortVideo.id == video_id).first()

def get_user_short_videos(db: Session, user_id: int):
    """Get all short videos for a specific user"""
    return db.query(ShortVideo).filter(ShortVideo.user_id == user_id).all()

def delete_short_video(db: Session, video_id: int):
    """Delete a short video"""
    video = db.query(ShortVideo).filter(ShortVideo.id == video_id).first()
    if video:
        db.delete(video)
        db.commit()
        return True
    return False