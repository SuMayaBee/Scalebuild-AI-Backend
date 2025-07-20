from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, func
from app.core.database import Base

class Presentation(Base):
    __tablename__ = "presentations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    theme = Column(String, default="default")
    language = Column(String, default="English")
    tone = Column(String, default="Professional")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_public = Column(Boolean, default=False)
    slug = Column(String, nullable=True)

class PresentationImage(Base):
    __tablename__ = "presentation_images"

    id = Column(Integer, primary_key=True, index=True)
    presentation_id = Column(Integer, ForeignKey("presentations.id"), nullable=False)
    image_url = Column(String, nullable=False)
    prompt = Column(String, nullable=False)
    filename = Column(String, nullable=True)
    model = Column(String, default="dall-e-3")
    size = Column(String, default="1024x1024")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
