"""
User Image Upload Service
"""
import io
import uuid
import os
from typing import Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
from app.core.gcs_client import get_shared_gcs_client


class UserImageService:
    def __init__(self):
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.max_dimensions = (2048, 2048)  # Max width/height
    
    def validate_image(self, file: UploadFile) -> None:
        """Validate uploaded image file."""
        # Check file extension
        if not any(file.filename.lower().endswith(ext) for ext in self.allowed_extensions):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(self.allowed_extensions)}"
            )
        
        # Check file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {self.max_file_size // (1024*1024)}MB"
            )
    
    def process_image(self, file_content: bytes) -> Tuple[io.BytesIO, str]:
        """Process and optimize the image."""
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(file_content))
            
            # Convert to RGB if necessary (for JPEG compatibility)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            if image.size[0] > self.max_dimensions[0] or image.size[1] > self.max_dimensions[1]:
                image.thumbnail(self.max_dimensions, Image.Resampling.LANCZOS)
            
            # Save optimized image
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output, 'image/jpeg'
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
    
    async def upload_user_image(self, file: UploadFile, user_id: int) -> str:
        """
        Upload user profile image to GCS.
        
        Args:
            file: Uploaded image file
            user_id: User ID for filename
            
        Returns:
            Public URL of uploaded image
        """
        # Validate the file
        self.validate_image(file)
        
        # Read file content
        file_content = await file.read()
        
        # Process the image
        processed_image, content_type = self.process_image(file_content)
        
        # Generate unique filename
        file_extension = '.jpg'  # Always save as JPEG after processing
        unique_id = str(uuid.uuid4())[:8]
        filename = f"user_images/user_{user_id}_{unique_id}{file_extension}"
        
        try:
            # Get GCS client and bucket
            storage_client = get_shared_gcs_client()
            bucket_name = os.getenv("GCS_BUCKET_NAME", "deck123")
            bucket = storage_client.bucket(bucket_name)
            
            # Create blob and upload
            blob = bucket.blob(filename)
            processed_image.seek(0)  # Reset file pointer to beginning
            
            blob.upload_from_file(
                processed_image,
                content_type=content_type
            )
            
            # Make the blob publicly accessible
            blob.make_public()
            
            public_url = blob.public_url
            print(f"✅ User image uploaded to GCS: {public_url}")
            
            return public_url
            
        except Exception as e:
            print(f"❌ Error uploading user image to GCS: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


# Global service instance
user_image_service = UserImageService()