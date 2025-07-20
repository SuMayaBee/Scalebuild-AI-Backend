from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func
from app.core.database import Base

class Logo(Base):
    __tablename__ = "logos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    logo_image_url = Column(String, nullable=False)
    remove_bg_logo_image_url = Column(String, nullable=True)
    content = Column(JSON, nullable=True)  # Store logo design specifications and metadata
    logo_title = Column(String, nullable=False)
    logo_vision = Column(String, nullable=True)
    color_palette_name = Column(String, nullable=True)
    logo_style = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())