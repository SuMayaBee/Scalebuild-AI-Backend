from sqlalchemy.orm import Session
from app.presentation.models import Presentation

def create_presentation(db: Session, user_id: int, prompt: str, image_url: str):
    presentation = Presentation(user_id=user_id, prompt=prompt, image_url=image_url)
    db.add(presentation)
    db.commit()
    db.refresh(presentation)
    return presentation
