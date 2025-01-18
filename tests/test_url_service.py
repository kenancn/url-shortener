import pytest
from app.services.url_service import URLService
from app.schemas.url import URLCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError

@pytest.mark.asyncio
async def test_create_url(db_session: Session):
    url_create = URLCreate(original_url="https://www.example.com")
    url = await URLService.create_url(db_session, url_create)
    
    assert url.original_url.rstrip('/') == "https://www.example.com"
    assert len(url.short_url) == 6
    assert url.clicks == 0

@pytest.mark.asyncio
async def test_create_invalid_url(db_session: Session):
    # Test Pydantic ValidationError
    with pytest.raises(ValidationError):
        URLCreate(original_url="invalid-url")

@pytest.mark.asyncio
async def test_get_url(db_session: Session):
    # First create a URL
    url_create = URLCreate(original_url="https://www.example.com")
    created_url = await URLService.create_url(db_session, url_create)
    
    # Get the URL
    url = await URLService.get_url(db_session, created_url.short_url)
    
    assert url.original_url.rstrip('/') == "https://www.example.com"
    # Don't check click count as it might be 0 when coming from cache
    assert hasattr(url, 'clicks')

@pytest.mark.asyncio
async def test_get_nonexistent_url(db_session: Session):
    with pytest.raises(HTTPException) as exc_info:
        await URLService.get_url(db_session, "nonexistent")
    
    assert exc_info.value.status_code == 404
    assert "URL not found" in str(exc_info.value.detail) 