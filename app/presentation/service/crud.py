from sqlalchemy.orm import Session
from app.presentation.db_models import Presentation, PresentationImage

def create_presentation(db: Session, user_id: int, prompt: str, image_url: str):
    presentation = Presentation(user_id=user_id, prompt=prompt, image_url=image_url)
    db.add(presentation)
    db.commit()
    db.refresh(presentation)
    return presentation

def create_presentation_image(
    db: Session, 
    presentation_id: int, 
    image_url: str, 
    prompt: str, 
    filename: str = None,
    model: str = "dall-e-3",
    size: str = "1024x1024"
):
    """Create a new presentation image record"""
    presentation_image = PresentationImage(
        presentation_id=presentation_id,
        image_url=image_url,
        prompt=prompt,
        filename=filename,
        model=model,
        size=size
    )
    db.add(presentation_image)
    db.commit()
    db.refresh(presentation_image)
    return presentation_image

def get_presentation_images(db: Session, presentation_id: int):
    """Get all images for a specific presentation"""
    try:
        # First check if presentation exists
        presentation_exists = db.query(Presentation).filter(Presentation.id == presentation_id).first()
        if not presentation_exists:
            return []  # Return empty list if presentation doesn't exist
        
        return db.query(PresentationImage).filter(PresentationImage.presentation_id == presentation_id).all()
    except Exception as e:
        # Log the error and re-raise
        print(f"Database error in get_presentation_images: {e}")
        db.rollback()  # Rollback the transaction
        raise

def get_presentation_image(db: Session, image_id: int):
    """Get a specific presentation image by ID"""
    return db.query(PresentationImage).filter(PresentationImage.id == image_id).first()
