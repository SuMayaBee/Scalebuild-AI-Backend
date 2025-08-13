from sqlalchemy.orm import Session
from app.auth.db_models import User
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, name: str = None):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, name: str = None, image_url: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if name is not None:
            user.name = name
        if image_url is not None:
            user.image_url = image_url
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None

def update_user_password(db: Session, user_id: int, current_password: str, new_password: str):
    """Update user password after verifying current password"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        return False  # Current password is incorrect
    
    # Update to new password
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def set_reset_token(db: Session, user: User, token: str):
    user.reset_token = token
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def validate_reset_token(db: Session, token: str):
    """Validate if reset token exists and return user info without resetting password"""
    user = db.query(User).filter(User.reset_token == token).first()
    if user:
        return {
            "valid": True,
            "user_id": user.id,
            "email": user.email,
            "name": user.name
        }
    return {"valid": False}

def reset_password_with_token(db: Session, token: str, new_password: str):
    """Reset password using validated token"""
    user = db.query(User).filter(User.reset_token == token).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None  # Clear the token after use
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None

# Keep the old function for backward compatibility
def reset_password(db: Session, token: str, new_password: str):
    return reset_password_with_token(db, token, new_password)
