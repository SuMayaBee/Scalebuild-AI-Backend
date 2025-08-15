"""
Web Scraper Service using LangChain WebBaseLoader
"""
import os
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin
import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

class WebScraperService:
    """Service to scrape websites using LangChain WebBaseLoader"""
    
    def __init__(self):
        """Initialize web scraper service"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        print("✅ Web scraper service initialized")
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Quick HEAD request to check if URL is accessible
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
            
        except Exception as e:
            print(f"❌ URL validation failed for {url}: {e}")
            return False
    
    def scrape_single_url(self, url: str, verify_ssl: bool = True) -> Dict[str, Any]:
        """
        Scrape content from a single URL
        
        Args:
            url: URL to scrape
            verify_ssl: Whether to verify SSL certificates
            
        Returns:
            Dictionary with scraped content and metadata
        """
        try:
            print(f"🌐 Scraping URL: {url}")
            
            # Validate URL first
            if not self.is_valid_url(url):
                raise ValueError(f"Invalid or inaccessible URL: {url}")
            
            # Configure loader with SSL verification option
            loader_kwargs = {}
            if not verify_ssl:
                loader_kwargs['requests_kwargs'] = {'verify': False}
            
            # Create WebBaseLoader
            loader = WebBaseLoader(url, **loader_kwargs)
            
            # Load documents
            documents = loader.load()
            
            if not documents:
                raise ValueError(f"No content found at URL: {url}")
            
            # Extract content from first document (WebBaseLoader typically returns one doc per URL)
            doc = documents[0]
            content = doc.page_content
            metadata = doc.metadata
            
            # Clean up content
            content = self._clean_content(content)
            
            if not content.strip():
                raise ValueError(f"No meaningful content extracted from URL: {url}")
            
            # Add additional metadata
            metadata.update({
                'url': url,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'content_length': len(content),
                'word_count': len(content.split())
            })
            
            print(f"✅ Successfully scraped {len(content)} characters from {url}")
            
            return {
                'content': content,
                'metadata': metadata,
                'url': url
            }
            
        except Exception as e:
            print(f"❌ Error scraping URL {url}: {e}")
            raise
    
    def scrape_multiple_urls(
        self, 
        urls: List[str], 
        verify_ssl: bool = True,
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Scrape content from multiple URLs
        
        Args:
            urls: List of URLs to scrape
            verify_ssl: Whether to verify SSL certificates
            max_concurrent: Maximum number of concurrent requests
            
        Returns:
            List of dictionaries with scraped content and metadata
        """
        try:
            print(f"🌐 Scraping {len(urls)} URLs...")
            
            # Filter valid URLs
            valid_urls = [url for url in urls if self.is_valid_url(url)]
            
            if not valid_urls:
                raise ValueError("No valid URLs provided")
            
            print(f"📋 {len(valid_urls)} valid URLs found")
            
            # Configure loader for multiple URLs
            loader_kwargs = {}
            if not verify_ssl:
                loader_kwargs['requests_kwargs'] = {'verify': False}
            
            # Create WebBaseLoader for multiple URLs
            loader = WebBaseLoader(valid_urls, **loader_kwargs)
            
            # Load all documents
            documents = loader.load()
            
            if not documents:
                raise ValueError("No content found from any URLs")
            
            results = []
            
            for doc in documents:
                content = self._clean_content(doc.page_content)
                
                if content.strip():  # Only include non-empty content
                    metadata = doc.metadata.copy()
                    url = metadata.get('source', 'unknown')
                    
                    metadata.update({
                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'content_length': len(content),
                        'word_count': len(content.split())
                    })
                    
                    results.append({
                        'content': content,
                        'metadata': metadata,
                        'url': url
                    })
            
            print(f"✅ Successfully scraped {len(results)} pages")
            return results
            
        except Exception as e:
            print(f"❌ Error scraping multiple URLs: {e}")
            raise
    
    def scrape_website_with_sitemap(self, base_url: str, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape website using sitemap or by discovering pages
        
        Args:
            base_url: Base URL of the website
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of dictionaries with scraped content and metadata
        """
        try:
            print(f"🕷️ Discovering pages from {base_url}...")
            
            # Try to find sitemap
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/robots.txt')
            ]
            
            discovered_urls = set([base_url])  # Start with base URL
            
            # Try to extract URLs from sitemap
            for sitemap_url in sitemap_urls:
                try:
                    response = requests.get(sitemap_url, timeout=10)
                    if response.status_code == 200:
                        # Simple extraction of URLs from sitemap/robots.txt
                        content = response.text
                        
                        # Extract URLs (basic implementation)
                        import re
                        urls = re.findall(r'https?://[^\s<>"]+', content)
                        
                        for url in urls:
                            if base_url in url and len(discovered_urls) < max_pages:
                                discovered_urls.add(url)
                        
                        if len(discovered_urls) >= max_pages:
                            break
                            
                except Exception as e:
                    print(f"⚠️ Could not access {sitemap_url}: {e}")
                    continue
            
            # Limit to max_pages
            urls_to_scrape = list(discovered_urls)[:max_pages]
            
            print(f"📋 Found {len(urls_to_scrape)} URLs to scrape")
            
            # Scrape all discovered URLs
            return self.scrape_multiple_urls(urls_to_scrape)
            
        except Exception as e:
            print(f"❌ Error scraping website with sitemap: {e}")
            # Fallback to just scraping the base URL
            return [self.scrape_single_url(base_url)]
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize scraped content"""
        if not content:
            return ""
        
        # Remove excessive whitespace
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and line not in cleaned_lines[-3:]:  # Remove duplicate consecutive lines
                cleaned_lines.append(line)
        
        # Join lines and normalize spacing
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Remove excessive newlines
        import re
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
        
        return cleaned_content.strip()
    
    def chunk_web_content(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk web content for embedding
        
        Args:
            content: Web content to chunk
            metadata: Metadata about the content
            
        Returns:
            List of chunks with metadata
        """
        try:
            # Split content into chunks
            chunks = self.text_splitter.split_text(content)
            
            result_chunks = []
            
            for i, chunk_content in enumerate(chunks):
                if chunk_content.strip():  # Only include non-empty chunks
                    chunk_metadata = metadata.copy()
                    chunk_metadata.update({
                        'chunk_index': i,
                        'chunk_content': chunk_content,
                        'char_count': len(chunk_content),
                        'token_count': len(chunk_content.split())  # Rough token estimate
                    })
                    
                    result_chunks.append({
                        'content': chunk_content,
                        'metadata': chunk_metadata,
                        'chunk_index': i,
                        'char_count': len(chunk_content),
                        'token_count': len(chunk_content.split())
                    })
            
            print(f"✅ Split content into {len(result_chunks)} chunks")
            return result_chunks
            
        except Exception as e:
            print(f"❌ Error chunking web content: {e}")
            raise
    
    def test_scraping(self, test_url: str = "https://example.com") -> bool:
        """Test web scraping functionality"""
        try:
            result = self.scrape_single_url(test_url)
            return bool(result and result.get('content'))
        except Exception as e:
            print(f"❌ Web scraping test failed: {e}")
            return False

# Global web scraper service instance
web_scraper_service = WebScraperService()