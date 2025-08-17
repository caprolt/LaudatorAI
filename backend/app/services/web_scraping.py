"""Web scraping service for job posting extraction."""

import asyncio
import logging
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import re

from playwright.async_api import async_playwright, Browser, Page
# from readability import Document  # Temporarily disabled due to lxml compatibility issue
import httpx

from app.core.logging import get_logger

logger = get_logger(__name__)


class WebScrapingService:
    """Service for scraping job postings from URLs."""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_job_posting(self, url: str) -> Dict[str, Any]:
        """
        Scrape a job posting URL and extract structured content.
        
        Args:
            url: The job posting URL to scrape
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        try:
            # First try with Playwright
            content = await self._scrape_with_playwright(url)
            if content and content.get('content'):
                return content
                
            # Fallback to Readability
            logger.warning(f"Playwright failed for {url}, trying Readability fallback")
            content = await self._scrape_with_readability(url)
            return content
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            raise
    
    async def _scrape_with_playwright(self, url: str) -> Dict[str, Any]:
        """Scrape using Playwright for dynamic content."""
        try:
            page = await self.browser.new_page()
            
            # Set user agent to avoid detection
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            # Navigate to the page
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for content to load
            await page.wait_for_timeout(2000)
            
            # Extract content based on common job posting selectors
            content = await self._extract_job_content(page)
            
            await page.close()
            return content
            
        except Exception as e:
            logger.error(f"Playwright scraping failed for {url}: {str(e)}")
            return {}
    
    async def _extract_job_content(self, page: Page) -> Dict[str, Any]:
        """Extract job content using common selectors."""
        content = {
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'requirements': '',
            'content': '',
            'metadata': {}
        }
        
        # Common selectors for job postings
        title_selectors = [
            'h1[class*="title"]',
            'h1[class*="job"]',
            'h1[class*="position"]',
            '.job-title',
            '.position-title',
            'h1',
            '[data-testid="job-title"]'
        ]
        
        company_selectors = [
            '[class*="company"]',
            '[class*="employer"]',
            '.company-name',
            '.employer-name',
            '[data-testid="company-name"]'
        ]
        
        location_selectors = [
            '[class*="location"]',
            '.job-location',
            '.location',
            '[data-testid="location"]'
        ]
        
        description_selectors = [
            '[class*="description"]',
            '.job-description',
            '.description',
            '[data-testid="job-description"]',
            'main',
            'article'
        ]
        
        # Extract title
        for selector in title_selectors:
            try:
                title_element = await page.query_selector(selector)
                if title_element:
                    content['title'] = await title_element.text_content()
                    content['title'] = content['title'].strip()
                    if content['title']:
                        break
            except Exception:
                continue
        
        # Extract company
        for selector in company_selectors:
            try:
                company_element = await page.query_selector(selector)
                if company_element:
                    content['company'] = await company_element.text_content()
                    content['company'] = content['company'].strip()
                    if content['company']:
                        break
            except Exception:
                continue
        
        # Extract location
        for selector in location_selectors:
            try:
                location_element = await page.query_selector(selector)
                if location_element:
                    content['location'] = await location_element.text_content()
                    content['location'] = content['location'].strip()
                    if content['location']:
                        break
            except Exception:
                continue
        
        # Extract description
        for selector in description_selectors:
            try:
                desc_element = await page.query_selector(selector)
                if desc_element:
                    content['description'] = await desc_element.inner_html()
                    if content['description']:
                        break
            except Exception:
                continue
        
        # Get full page content as fallback
        if not content['description']:
            content['content'] = await page.content()
        
        # Extract metadata
        content['metadata'] = await self._extract_metadata(page)
        
        return content
    
    async def _extract_metadata(self, page: Page) -> Dict[str, Any]:
        """Extract metadata from the page."""
        metadata = {}
        
        try:
            # Extract meta tags
            meta_tags = await page.query_selector_all('meta')
            for meta in meta_tags:
                name = await meta.get_attribute('name') or await meta.get_attribute('property')
                content = await meta.get_attribute('content')
                if name and content:
                    metadata[name] = content
            
            # Extract structured data (JSON-LD)
            json_ld_scripts = await page.query_selector_all('script[type="application/ld+json"]')
            for script in json_ld_scripts:
                try:
                    content = await script.text_content()
                    if content:
                        import json
                        data = json.loads(content)
                        if isinstance(data, dict):
                            metadata['json_ld'] = data
                except Exception:
                    continue
                    
        except Exception as e:
            logger.warning(f"Failed to extract metadata: {str(e)}")
        
        return metadata
    
    async def _scrape_with_readability(self, url: str) -> Dict[str, Any]:
        """Fallback scraping using Readability."""
        # Temporarily disabled due to lxml compatibility issue
        logger.warning(f"Readability fallback disabled for {url}")
        return {
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'requirements': '',
            'content': '',
            'metadata': {},
            'error': 'Readability fallback temporarily disabled'
        }


async def scrape_job_posting(url: str) -> Dict[str, Any]:
    """
    Convenience function to scrape a job posting.
    
    Args:
        url: The job posting URL to scrape
        
    Returns:
        Dictionary containing scraped content and metadata
    """
    async with WebScrapingService() as scraper:
        return await scraper.scrape_job_posting(url)
