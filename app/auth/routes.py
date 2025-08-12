from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth import schemas, crud
from app.core.security import create_access_token, get_current_user
from app.auth.models import User
from app.auth.image_service import user_image_service
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/signup", response_model=schemas.UserRead)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    new_user = crud.create_user(db, user.email, user.password, user.fullname)
    return new_user

@router.post("/signin", response_model=schemas.Token)
def signin(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token({"sub": db_user.email}, user_id=db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Generate an 8-digit numeric reset token
    token = str(random.randint(10000000, 99999999))
    crud.set_reset_token(db, user, token)
    return {"msg": "Password reset token generated", "token": token}

@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    user = crud.reset_password(db, request.token, request.new_password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"msg": "Password reset successful"}

@router.post("/upload-image")
async def upload_user_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload user profile image."""
    try:
        # Upload image to GCS
        image_url = await user_image_service.upload_user_image(file, current_user.id)
        
        # Update user's image URL in database
        updated_user = crud.update_user(db, current_user.id, image_url=image_url)
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "message": "Image uploaded successfully",
            "image_url": image_url,
            "user": schemas.UserRead.from_orm(updated_user)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.get("/profile", response_model=schemas.UserRead)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile."""
    return current_user

@router.put("/profile", response_model=schemas.UserRead)
def update_user_profile(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile information."""
    updated_user = crud.update_user(
        db, 
        current_user.id, 
        fullname=user_update.fullname,
        image_url=user_update.image_url
    )
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user
