"""
Web Scraping Service for RAG System
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import time
from urllib.parse import urljoin, urlparse
import re

class WebScraperService:
    """Service to scrape content from websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 30
        self.max_content_length = 10 * 1024 * 1024  # 10MB max per page
        
        print("✅ Web scraper service initialized")
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\'\/]', '', text)
        return text.strip()
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()
        
        # Try to find main content areas
        main_content = ""
        
        # Look for main content containers
        content_selectors = [
            'main', 'article', '[role="main"]', '.content', '.main-content',
            '.post-content', '.entry-content', '.article-content', '#content'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    main_content += element.get_text(separator=' ', strip=True) + "\n"
                break
        
        # If no main content found, extract from body
        if not main_content.strip():
            body = soup.find('body')
            if body:
                main_content = body.get_text(separator=' ', strip=True)
        
        # If still no content, get all text
        if not main_content.strip():
            main_content = soup.get_text(separator=' ', strip=True)
        
        return self._clean_text(main_content)
    
    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a single URL
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped content and metadata
        """
        try:
            if not self._is_valid_url(url):
                raise ValueError(f"Invalid URL: {url}")
            
            print(f"🌐 Scraping URL: {url}")
            
            # Make request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Check content length
            if len(response.content) > self.max_content_length:
                raise ValueError(f"Content too large: {len(response.content)} bytes")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
            
            description = ""
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                description = desc_tag.get('content', '').strip()
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            if not content.strip():
                raise ValueError("No content could be extracted from the page")
            
            # Get domain for metadata
            domain = urlparse(url).netloc
            
            metadata = {
                "url": url,
                "domain": domain,
                "title": title,
                "description": description,
                "content_length": len(content),
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status_code": response.status_code
            }
            
            print(f"✅ Scraped {len(content)} characters from {domain}")
            
            return {
                "content": content,
                "metadata": metadata,
                "success": True
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error for {url}: {e}")
            return {
                "content": "",
                "metadata": {"url": url, "error": str(e)},
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            print(f"❌ Scraping error for {url}: {e}")
            return {
                "content": "",
                "metadata": {"url": url, "error": str(e)},
                "success": False,
                "error": str(e)
            }
    
    def scrape_multiple_urls(self, urls: List[str], delay: float = 1.0) -> List[Dict[str, Any]]:
        """
        Scrape content from multiple URLs
        
        Args:
            urls: List of URLs to scrape
            delay: Delay between requests in seconds
            
        Returns:
            List of scraping results
        """
        results = []
        
        print(f"🌐 Scraping {len(urls)} URLs...")
        
        for i, url in enumerate(urls):
            try:
                result = self.scrape_url(url)
                results.append(result)
                
                # Add delay between requests to be respectful
                if i < len(urls) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Failed to scrape {url}: {e}")
                results.append({
                    "content": "",
                    "metadata": {"url": url, "error": str(e)},
                    "success": False,
                    "error": str(e)
                })
        
        successful = sum(1 for r in results if r["success"])
        print(f"✅ Successfully scraped {successful}/{len(urls)} URLs")
        
        return results
    
    def get_page_links(self, url: str, same_domain_only: bool = True) -> List[str]:
        """
        Extract links from a webpage
        
        Args:
            url: URL to extract links from
            same_domain_only: Only return links from the same domain
            
        Returns:
            List of URLs found on the page
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            base_domain = urlparse(url).netloc
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Convert relative URLs to absolute
                full_url = urljoin(url, href)
                
                # Skip non-HTTP URLs
                if not full_url.startswith(('http://', 'https://')):
                    continue
                
                # Filter by domain if requested
                if same_domain_only:
                    link_domain = urlparse(full_url).netloc
                    if link_domain != base_domain:
                        continue
                
                if full_url not in links:
                    links.append(full_url)
            
            print(f"✅ Found {len(links)} links on {url}")
            return links
            
        except Exception as e:
            print(f"❌ Error extracting links from {url}: {e}")
            return []

# Global web scraper service instance
web_scraper = WebScraperService()