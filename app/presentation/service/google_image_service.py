"""
Google Images Search Service for Fast Image Retrieval
Alternative to AI image generation for better performance
"""
import os
import io
import asyncio
import aiohttp
import uuid
from typing import Optional, List, Dict
from datetime import datetime
from google.cloud import storage
from urllib.parse import quote_plus
import re

class GoogleImageSearchService:
    def __init__(self):
        # Google Custom Search API credentials
        self.api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        # GCS setup for storing fetched images
        from app.core.gcs_client import get_shared_gcs_client
        self.storage_client = get_shared_gcs_client()
        self.gcs_bucket_name = os.getenv("GCS_BUCKET_NAME", "deck123")
        self.bucket = self.storage_client.bucket(self.gcs_bucket_name)
        
        print("🔍 Google Image Search Service initialized")
        if not self.api_key or not self.search_engine_id:
            print("⚠️ Warning: Google Search API credentials not configured")
    
    def _clean_search_query(self, prompt: str) -> str:
        """Clean and optimize search query for better results"""
        # Remove special characters and extra spaces
        cleaned = re.sub(r'[^\w\s-]', ' ', prompt)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Add relevant keywords for better image results
        keywords = ["high quality", "professional", "stock photo"]
        
        # Limit query length (Google has limits)
        if len(cleaned) > 100:
            cleaned = cleaned[:100].rsplit(' ', 1)[0]
        
        return cleaned
    
    async def search_images(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for images using Google Custom Search API"""
        if not self.api_key or not self.search_engine_id:
            raise Exception("Google Search API credentials not configured")
        
        cleaned_query = self._clean_search_query(query)
        
        params = {
            'key': self.api_key,
            'cx': self.search_engine_id,
            'q': cleaned_query,
            'searchType': 'image',
            'num': min(num_results, 10),  # Google allows max 10 per request
            'imgSize': 'large',
            'imgType': 'photo',
            'safe': 'active',
            'rights': 'cc_publicdomain,cc_attribute,cc_sharealike,cc_noncommercial,cc_nonderived'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        images = []
                        if 'items' in data:
                            for item in data['items']:
                                images.append({
                                    'url': item.get('link'),
                                    'title': item.get('title', ''),
                                    'thumbnail': item.get('image', {}).get('thumbnailLink'),
                                    'context': item.get('image', {}).get('contextLink'),
                                    'size': f"{item.get('image', {}).get('width', 0)}x{item.get('image', {}).get('height', 0)}"
                                })
                        
                        print(f"🔍 Found {len(images)} images for query: {cleaned_query}")
                        return images
                    else:
                        error_data = await response.json()
                        raise Exception(f"Google Search API error: {error_data}")
        
        except Exception as e:
            print(f"❌ Error searching images: {str(e)}")
            raise e
    
    async def download_and_store_image(self, image_url: str, filename: str = None) -> str:
        """Download image from URL and store in GCS"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        
                        # Generate filename if not provided
                        if not filename:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            unique_id = str(uuid.uuid4())[:8]
                            filename = f"google_images/img_{timestamp}_{unique_id}.jpg"
                        elif not filename.startswith("google_images/"):
                            filename = f"google_images/{filename}"
                        
                        # Upload to GCS
                        blob = self.bucket.blob(filename)
                        blob.upload_from_string(
                            image_data,
                            content_type=response.headers.get('content-type', 'image/jpeg')
                        )
                        
                        # Make publicly accessible
                        blob.make_public()
                        
                        public_url = blob.public_url
                        print(f"📁 Image stored in GCS: {public_url}")
                        
                        return public_url
                    else:
                        raise Exception(f"Failed to download image: HTTP {response.status}")
        
        except Exception as e:
            print(f"❌ Error downloading/storing image: {str(e)}")
            raise e
    
    async def get_presentation_image_fast(
        self, 
        prompt: str, 
        store_in_gcs: bool = True,
        filename: str = None
    ) -> Dict:
        """
        Fast image retrieval for presentations
        Returns the best matching image from Google search
        """
        try:
            print(f"🚀 Fast image search for: {prompt}")
            
            # Search for images
            images = await self.search_images(prompt, num_results=3)
            
            if not images:
                raise Exception("No images found for the given prompt")
            
            # Get the best image (first result is usually most relevant)
            best_image = images[0]
            image_url = best_image['url']
            
            if store_in_gcs:
                # Download and store in our GCS bucket
                stored_url = await self.download_and_store_image(image_url, filename)
                
                return {
                    'success': True,
                    'url': stored_url,
                    'original_url': image_url,
                    'prompt': prompt,
                    'title': best_image.get('title', ''),
                    'size': best_image.get('size', ''),
                    'source': 'google_search',
                    'filename': filename,
                    'alternatives': images[1:] if len(images) > 1 else []
                }
            else:
                # Return direct URL without storing
                return {
                    'success': True,
                    'url': image_url,
                    'prompt': prompt,
                    'title': best_image.get('title', ''),
                    'size': best_image.get('size', ''),
                    'source': 'google_search_direct',
                    'alternatives': images[1:] if len(images) > 1 else []
                }
        
        except Exception as e:
            print(f"❌ Fast image retrieval failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'prompt': prompt
            }
    
    async def get_multiple_images(
        self, 
        prompts: List[str], 
        store_in_gcs: bool = True
    ) -> List[Dict]:
        """
        Get multiple images concurrently for better performance
        """
        tasks = []
        for i, prompt in enumerate(prompts):
            filename = f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg" if store_in_gcs else None
            task = self.get_presentation_image_fast(prompt, store_in_gcs, filename)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'success': False,
                    'error': str(result),
                    'prompt': prompts[i]
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def test_api_connection(self) -> bool:
        """Test Google Search API connection"""
        try:
            if not self.api_key or not self.search_engine_id:
                print("❌ Google Search API credentials not configured")
                return False
            
            # Simple test query
            import requests
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': 'test',
                'searchType': 'image',
                'num': 1
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                print("✅ Google Search API connection successful")
                return True
            else:
                print(f"❌ Google Search API test failed: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ Google Search API connection test failed: {e}")
            return False

# Global service instance
google_image_service = GoogleImageSearchService()

# Utility functions for easy import
async def search_presentation_image(prompt: str, store_in_gcs: bool = True) -> Dict:
    """Quick function to search for a presentation image"""
    return await google_image_service.get_presentation_image_fast(prompt, store_in_gcs)

async def search_multiple_images(prompts: List[str], store_in_gcs: bool = True) -> List[Dict]:
    """Quick function to search for multiple images"""
    return await google_image_service.get_multiple_images(prompts, store_in_gcs)