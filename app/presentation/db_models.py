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
