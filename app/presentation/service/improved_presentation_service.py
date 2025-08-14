"""
Improved Presentation Service with better error handling and performance
"""
import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.presentation.db_models import Presentation, PresentationImage
from app.core.database import SessionLocal
from app.presentation.service.enhanced_image_service import enhanced_image_service
from app.presentation.service.google_image_service import google_image_service

class PresentationServiceError(Exception):
    """Custom exception for presentation service errors"""
    pass

class PresentationNotFoundError(PresentationServiceError):
    """Raised when presentation is not found"""
    pass

class ImageGenerationError(PresentationServiceError):
    """Raised when image generation fails"""
    pass

class ImprovedPresentationService:
    """Enhanced presentation service with better error handling and performance"""
    
    def __init__(self):
        self.max_retries = 3
        self.cache = {}  # Simple in-memory cache (consider Redis for production)
    
    async def create_presentation_with_validation(
        self,
        title: str,
        content: Dict[str, Any],
        user_id: int,
        theme: str = "default",
        language: str = "English",
        tone: str = "Professional"
    ) -> Dict[str, Any]:
        """Create presentation with proper validation and error handling"""
        
        # Validate inputs
        if not title or not title.strip():
            raise PresentationServiceError("Title is required and cannot be empty")
        
        if not isinstance(user_id, int) or user_id <= 0:
            raise PresentationServiceError("Valid user_id is required")
        
        if not content or not isinstance(content, dict):
            content = {"slides": []}
        
        # Validate theme, language, tone
        valid_themes = ["default", "modern", "classic", "minimal", "corporate"]
        valid_languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        valid_tones = ["Professional", "Casual", "Academic", "Creative", "Technical"]
        
        if theme not in valid_themes:
            theme = "default"
        if language not in valid_languages:
            language = "English"
        if tone not in valid_tones:
            tone = "Professional"
        
        db: Session = SessionLocal()
        try:
            presentation = Presentation(
                title=title.strip(),
                content=content,
                user_id=user_id,
                theme=theme,
                language=language,
                tone=tone,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(presentation)
            db.commit()
            db.refresh(presentation)
            
            return {
                "id": presentation.id,
                "title": presentation.title,
                "content": presentation.content,
                "theme": presentation.theme,
                "language": presentation.language,
                "tone": presentation.tone,
                "user_id": presentation.user_id,
                "created_at": presentation.created_at.isoformat(),
                "updated_at": presentation.updated_at.isoformat(),
                "is_public": presentation.is_public,
                "slug": presentation.slug
            }
            
        except SQLAlchemyError as e:
            db.rollback()
            raise PresentationServiceError(f"Database error: {str(e)}")
        except Exception as e:
            db.rollback()
            raise PresentationServiceError(f"Unexpected error: {str(e)}")
        finally:
            db.close()
    
    async def get_presentation_with_images(self, presentation_id: int) -> Optional[Dict[str, Any]]:
        """Get presentation with associated images"""
        db: Session = SessionLocal()
        try:
            presentation = db.query(Presentation).filter(Presentation.id == presentation_id).first()
            
            if not presentation:
                raise PresentationNotFoundError(f"Presentation with id {presentation_id} not found")
            
            # Get associated images
            images = db.query(PresentationImage).filter(
                PresentationImage.presentation_id == presentation_id
            ).all()
            
            return {
                "id": presentation.id,
                "title": presentation.title,
                "content": presentation.content,
                "theme": presentation.theme,
                "language": presentation.language,
                "tone": presentation.tone,
                "user_id": presentation.user_id,
                "created_at": presentation.created_at.isoformat(),
                "updated_at": presentation.updated_at.isoformat(),
                "is_public": presentation.is_public,
                "slug": presentation.slug,
                "images": [
                    {
                        "id": img.id,
                        "url": img.image_url,
                        "prompt": img.prompt,
                        "filename": img.filename,
                        "model": img.model,
                        "size": img.size,
                        "created_at": img.created_at.isoformat()
                    } for img in images
                ]
            }
            
        except SQLAlchemyError as e:
            raise PresentationServiceError(f"Database error: {str(e)}")
        finally:
            db.close()
    
    async def generate_image_with_fallback(
        self,
        prompt: str,
        presentation_id: Optional[int] = None,
        prefer_ai: bool = True,
        size: str = "1024x1024"
    ) -> Dict[str, Any]:
        """Generate image with fallback strategy"""
        
        if not prompt or not prompt.strip():
            raise ImageGenerationError("Prompt is required for image generation")
        
        # Try AI generation first if preferred
        if prefer_ai:
            try:
                print(f"🎨 Attempting AI image generation for: {prompt}")
                image_url = await enhanced_image_service.generate_presentation_image(
                    prompt=prompt,
                    model="dalle3",
                    size=size
                )
                
                # Save to database if presentation_id provided
                if presentation_id and image_url:
                    await self._save_image_to_db(
                        presentation_id=presentation_id,
                        image_url=image_url,
                        prompt=prompt,
                        model="dall-e-3",
                        size=size
                    )
                
                return {
                    "success": True,
                    "url": image_url,
                    "prompt": prompt,
                    "method": "ai_generation",
                    "model": "dall-e-3",
                    "size": size
                }
                
            except Exception as e:
                print(f"⚠️ AI generation failed, trying Google search fallback: {e}")
                
                # Fallback to Google search
                try:
                    result = await google_image_service.get_presentation_image_fast(
                        prompt=prompt,
                        store_in_gcs=True
                    )
                    
                    if result.get("success") and presentation_id:
                        await self._save_image_to_db(
                            presentation_id=presentation_id,
                            image_url=result["url"],
                            prompt=prompt,
                            model="google_search",
                            size="unknown"
                        )
                    
                    return {
                        "success": result.get("success", False),
                        "url": result.get("url"),
                        "prompt": prompt,
                        "method": "google_search_fallback",
                        "model": "google_search",
                        "error": result.get("error") if not result.get("success") else None
                    }
                    
                except Exception as fallback_error:
                    raise ImageGenerationError(f"Both AI and search fallback failed: {str(fallback_error)}")
        
        else:
            # Try Google search first
            try:
                print(f"🔍 Attempting Google search for: {prompt}")
                result = await google_image_service.get_presentation_image_fast(
                    prompt=prompt,
                    store_in_gcs=True
                )
                
                if result.get("success") and presentation_id:
                    await self._save_image_to_db(
                        presentation_id=presentation_id,
                        image_url=result["url"],
                        prompt=prompt,
                        model="google_search",
                        size="unknown"
                    )
                
                return {
                    "success": result.get("success", False),
                    "url": result.get("url"),
                    "prompt": prompt,
                    "method": "google_search",
                    "model": "google_search",
                    "error": result.get("error") if not result.get("success") else None
                }
                
            except Exception as e:
                print(f"⚠️ Google search failed, trying AI fallback: {e}")
                
                # Fallback to AI generation
                try:
                    image_url = await enhanced_image_service.generate_presentation_image(
                        prompt=prompt,
                        model="dalle3",
                        size=size
                    )
                    
                    if presentation_id and image_url:
                        await self._save_image_to_db(
                            presentation_id=presentation_id,
                            image_url=image_url,
                            prompt=prompt,
                            model="dall-e-3",
                            size=size
                        )
                    
                    return {
                        "success": True,
                        "url": image_url,
                        "prompt": prompt,
                        "method": "ai_generation_fallback",
                        "model": "dall-e-3",
                        "size": size
                    }
                    
                except Exception as fallback_error:
                    raise ImageGenerationError(f"Both search and AI fallback failed: {str(fallback_error)}")
    
    async def _save_image_to_db(
        self,
        presentation_id: int,
        image_url: str,
        prompt: str,
        model: str,
        size: str,
        filename: str = None
    ):
        """Save image metadata to database"""
        db: Session = SessionLocal()
        try:
            presentation_image = PresentationImage(
                presentation_id=presentation_id,
                image_url=image_url,
                prompt=prompt,
                filename=filename,
                model=model,
                size=size,
                created_at=datetime.utcnow()
            )
            
            db.add(presentation_image)
            db.commit()
            
        except SQLAlchemyError as e:
            db.rollback()
            print(f"❌ Failed to save image to database: {e}")
        finally:
            db.close()
    
    async def get_user_presentations_with_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user presentations with statistics"""
        db: Session = SessionLocal()
        try:
            presentations = db.query(Presentation).filter(Presentation.user_id == user_id).all()
            
            # Calculate statistics
            total_presentations = len(presentations)
            total_images = db.query(PresentationImage).join(Presentation).filter(
                Presentation.user_id == user_id
            ).count()
            
            # Group by theme
            theme_stats = {}
            language_stats = {}
            
            for presentation in presentations:
                theme_stats[presentation.theme] = theme_stats.get(presentation.theme, 0) + 1
                language_stats[presentation.language] = language_stats.get(presentation.language, 0) + 1
            
            presentation_list = []
            for presentation in presentations:
                # Get image count for each presentation
                image_count = db.query(PresentationImage).filter(
                    PresentationImage.presentation_id == presentation.id
                ).count()
                
                presentation_list.append({
                    "id": presentation.id,
                    "title": presentation.title,
                    "theme": presentation.theme,
                    "language": presentation.language,
                    "tone": presentation.tone,
                    "created_at": presentation.created_at.isoformat(),
                    "updated_at": presentation.updated_at.isoformat(),
                    "is_public": presentation.is_public,
                    "image_count": image_count
                })
            
            return {
                "presentations": presentation_list,
                "statistics": {
                    "total_presentations": total_presentations,
                    "total_images": total_images,
                    "theme_distribution": theme_stats,
                    "language_distribution": language_stats
                }
            }
            
        except SQLAlchemyError as e:
            raise PresentationServiceError(f"Database error: {str(e)}")
        finally:
            db.close()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all presentation services"""
        health_status = {
            "database": False,
            "openai": False,
            "google_search": False,
            "gcs": False,
            "overall": False
        }
        
        # Test database connection
        try:
            db: Session = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            health_status["database"] = True
        except Exception as e:
            print(f"Database health check failed: {e}")
        
        # Test OpenAI connection
        try:
            health_status["openai"] = enhanced_image_service.test_openai_connection()
        except Exception as e:
            print(f"OpenAI health check failed: {e}")
        
        # Test Google Search API
        try:
            health_status["google_search"] = google_image_service.test_api_connection()
        except Exception as e:
            print(f"Google Search health check failed: {e}")
        
        # Test GCS connection
        try:
            health_status["gcs"] = enhanced_image_service.test_gcs_connection()
        except Exception as e:
            print(f"GCS health check failed: {e}")
        
        # Overall health
        health_status["overall"] = (
            health_status["database"] and 
            health_status["gcs"] and 
            (health_status["openai"] or health_status["google_search"])
        )
        
        return health_status

# Global service instance
improved_presentation_service = ImprovedPresentationService()