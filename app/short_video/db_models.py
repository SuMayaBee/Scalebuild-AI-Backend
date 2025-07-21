from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from app.core.database import Base

class ShortVideo(Base):
    __tablename__ = "short_videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    aspect_ratio = Column(String, default="16:9")
    duration = Column(String, default="8")
    audio_generation = Column(Boolean, default=True)
    watermark = Column(Boolean, default=True)
    person_generation = Column(String, default="allow_all")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())