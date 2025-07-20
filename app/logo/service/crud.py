from sqlalchemy.orm import Session
from app.logo.db_models import Logo
from typing import Optional, Dict, Any

def create_logo(
    db: Session,
    user_id: int,
    logo_image_url: str,
    logo_title: str,
    logo_vision: Optional[str] = None,
    color_palette_name: Optional[str] = None,
    logo_style: Optional[str] = None,
    content: Optional[Dict[str, Any]] = None
):
    """Create a new logo record"""
    logo = Logo(
        user_id=user_id,
        logo_image_url=logo_image_url,
        logo_title=logo_title,
        logo_vision=logo_vision,
        color_palette_name=color_palette_name,
        logo_style=logo_style,
        content=content
    )
    db.add(logo)
    db.commit()
    db.refresh(logo)
    return logo

def get_logo(db: Session, logo_id: int):
    """Get a specific logo by ID"""
    return db.query(Logo).filter(Logo.id == logo_id).first()

def get_user_logos(db: Session, user_id: int):
    """Get all logos for a specific user"""
    return db.query(Logo).filter(Logo.user_id == user_id).all()

def update_logo_remove_bg_url(db: Session, logo_id: int, remove_bg_url: str):
    """Update the remove background URL for a logo"""
    logo = db.query(Logo).filter(Logo.id == logo_id).first()
    if logo:
        logo.remove_bg_logo_image_url = remove_bg_url
        db.commit()
        db.refresh(logo)
    return logo

def delete_logo(db: Session, logo_id: int):
    """Delete a logo"""
    logo = db.query(Logo).filter(Logo.id == logo_id).first()
    if logo:
        db.delete(logo)
        db.commit()
        return True
    return False