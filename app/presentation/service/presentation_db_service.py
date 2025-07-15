from typing import List, Optional, Dict, Any
import json
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.presentation.db_models import Presentation
from app.core.database import SessionLocal

class PresentationDBService:
    """Database service for managing presentations and generated images"""
    
    def __init__(self):
        self._connected = False
    
    def _format_presentation_result(self, presentation_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to format presentation data for API response"""
        result = presentation_dict.copy()
        
        # Parse content back to dict if it was stored as JSON string
        if isinstance(result.get("content"), str):
            try:
                result["content"] = json.loads(result["content"])
            except:
                result["content"] = {"slides": []}
        
        # Convert datetime objects to ISO string format
        if result.get("createdAt"):
            result["createdAt"] = result["createdAt"].isoformat() if hasattr(result["createdAt"], 'isoformat') else str(result["createdAt"])
        if result.get("updatedAt"):
            result["updatedAt"] = result["updatedAt"].isoformat() if hasattr(result["updatedAt"], 'isoformat') else str(result["updatedAt"])
        
        return result
    
    async def connect(self):
        """Connect to the database"""
        if not self._connected:
            # SQLAlchemy does not require explicit connect in the same way as Prisma
            self._connected = True
    
    async def disconnect(self):
        """Disconnect from the database"""
        if self._connected:
            # SQLAlchemy does not require explicit disconnect in the same way as Prisma
            self._connected = False
    
    async def ensure_connected(self):
        """Ensure database connection is active"""
        if not self._connected:
            await self.connect()
    
    # User Management
    async def get_or_create_user(self, email: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Get or create a user by email"""
        await self.ensure_connected()
        
        # User management is not rewritten for SQLAlchemy as it's not in the code block
        raise NotImplementedError("User management not implemented")
    
    # Presentation Management
    async def create_presentation(
        self, 
        title: str, 
        content: Dict[str, Any], 
        user_id: int,
        theme: str = "default",
        language: str = "English",
        tone: str = "Professional"
    ) -> Presentation:  # Return type is Presentation model instance
        """Create a new presentation"""
        await self.ensure_connected()
        
        # Ensure content is properly formatted JSON
        if not content:
            content = {"slides": []}
        
        db: Session = SessionLocal()
        try:
            # Ensure content is a dict, not a string
            if isinstance(content, str):
                content = json.loads(content)
            presentation = Presentation(
                title=title,
                content=content,  # store as dict
                user_id=user_id,
                theme=theme,
                language=language,
                tone=tone
            )
            db.add(presentation)
            db.commit()
            db.refresh(presentation)
            result = presentation  # Return the model instance, not a dict
        finally:
            db.close()
        
        return result
    
    async def get_presentation(self, presentation_id: str) -> Optional[Presentation]:
        """Get presentation by ID"""
        await self.ensure_connected()
        
        db: Session = SessionLocal()
        try:
            presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
            if not presentation:
                return None
            
            return presentation  # Return the model instance, not a dict
        finally:
            db.close()
    
    async def update_presentation(
        self, 
        presentation_id: str, 
        content: Optional[Dict[str, Any]] = None,
        title: Optional[str] = None
    ) -> Presentation:  # Return type is Presentation model instance
        """Update presentation content"""
        await self.ensure_connected()
        
        update_data = {}
        if content:
            update_data["content"] = json.dumps(content) if isinstance(content, dict) else content
        if title:
            update_data["title"] = title
            
        db: Session = SessionLocal()
        try:
            presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
            if not presentation:
                return None
            
            for key, value in update_data.items():
                setattr(presentation, key, value)
            
            db.commit()
            db.refresh(presentation)
            
            return presentation  # Return the model instance, not a dict
        finally:
            db.close()
    
    async def get_user_presentations(self, user_email: str) -> List[Presentation]:
        """Get all presentations for a user"""
        await self.ensure_connected()
        
        # User management is not rewritten for SQLAlchemy as it's not in the code block
        raise NotImplementedError("User management not implemented")
    
    async def delete_presentation(self, presentation_id: str) -> bool:
        """Delete a presentation"""
        await self.ensure_connected()
        
        db: Session = SessionLocal()
        try:
            presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
            if not presentation:
                return False
            
            db.delete(presentation)
            db.commit()
            return True
        except:
            return False
        finally:
            db.close()
    
    # Generated Image Management
    async def save_generated_image(
        self, 
        url: str, 
        prompt: str, 
        user_email: str,
        model: str = "dall-e-3",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save generated image metadata"""
        await self.ensure_connected()
        
        # Get or create user
        user = await self.get_or_create_user(user_email)
        
        image_data = {
            "url": url,
            "prompt": prompt,
            "userId": user["id"],
            "model": model
        }
        
        # Add metadata if provided
        if metadata:
            image_data.update(metadata)
        
        # Image management is not rewritten for SQLAlchemy as it's not in the code block
        raise NotImplementedError("Image management not implemented")
    
    async def get_user_images(self, user_email: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get generated images for a user"""
        await self.ensure_connected()
        
        # User management is not rewritten for SQLAlchemy as it's not in the code block
        raise NotImplementedError("User management not implemented")
    
    async def get_image_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Get image metadata by URL"""
        await self.ensure_connected()
        
        # Image management is not rewritten for SQLAlchemy as it's not in the code block
        raise NotImplementedError("Image management not implemented")

# Global service instance
presentation_db_service = PresentationDBService()

# Utility function for managing database connection lifecycle
async def with_db_connection(func, *args, **kwargs):
    """Execute a function with database connection management"""
    await presentation_db_service.connect()
    try:
        result = await func(*args, **kwargs)
        return result
    finally:
        await presentation_db_service.disconnect()