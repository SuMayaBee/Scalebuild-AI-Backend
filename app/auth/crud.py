from sqlalchemy.orm import Session
from app.auth.models import User
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

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

def reset_password(db: Session, token: str, new_password: str):
    user = db.query(User).filter(User.reset_token == token).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None
