from sqlalchemy.orm import Session
from app.models.url import URL
from app.schemas.url import URLCreate
from app.core.utils import generate_short_url, cache_url, get_cached_url
from fastapi import HTTPException
import validators
import logging
import time
from datetime import datetime, UTC
import asyncio

# Create logger
logger = logging.getLogger(__name__)

class URLService:
    @staticmethod
    async def create_url(db: Session, url_create: URLCreate) -> URL:
        """Creates a new short URL"""
        if not validators.url(str(url_create.original_url)):
            raise HTTPException(status_code=400, detail="Invalid URL format")

        # Generate unique short URL
        while True:
            short_url = generate_short_url()
            exists = db.query(URL).filter(URL.short_url == short_url).first()
            if not exists:
                break

        db_url = URL(
            original_url=str(url_create.original_url),
            short_url=short_url
        )
        
        db.add(db_url)
        db.commit()
        db.refresh(db_url)

        # Add URL to cache
        cache_url(short_url, str(url_create.original_url))
        
        return db_url

    @staticmethod
    async def get_url(db: Session, short_url: str) -> URL:
        """Gets original URL from short URL"""
        start_time = time.time()
        
        # Check cache first
        cached_url = get_cached_url(short_url)
        if cached_url:
            logger.info(f"Cache HIT for URL: {short_url}")
            # Update metrics asynchronously
            asyncio.create_task(URLService._update_metrics(db, short_url, start_time))
            return URL(original_url=cached_url, short_url=short_url)

        logger.info(f"Cache MISS for URL: {short_url}")
        # Check database
        db_url = db.query(URL).filter(URL.short_url == short_url).first()
        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")

        # Update metrics asynchronously
        asyncio.create_task(URLService._update_metrics(db, short_url, start_time))

        # Add to cache
        cache_url(short_url, str(db_url.original_url))
        logger.info(f"URL cached: {short_url}")

        return db_url

    @staticmethod
    async def _update_metrics(db: Session, short_url: str, start_time: float) -> None:
        """Updates URL metrics asynchronously"""
        try:
            db_url = db.query(URL).filter(URL.short_url == short_url).first()
            if db_url:
                # Increment click count
                db_url.clicks += 1
                
                # Update last access time
                db_url.last_accessed = datetime.now(UTC)
                
                # Calculate new average response time
                response_time = time.time() - start_time
                if db_url.avg_response_time == 0:
                    db_url.avg_response_time = response_time
                else:
                    n = db_url.clicks - 1
                    db_url.avg_response_time = ((db_url.avg_response_time * n) + response_time) / (n + 1)
                
                db.commit()
                logger.info(f"Metrics updated for URL: {short_url}")
        except Exception as e:
            logger.error(f"Error updating metrics for URL {short_url}: {str(e)}")

    @staticmethod
    async def get_url_stats(db: Session, short_url: str) -> URL:
        """Gets URL statistics"""
        db_url = db.query(URL).filter(URL.short_url == short_url).first()
        if not db_url:
            raise HTTPException(status_code=404, detail="URL not found")
        return db_url 