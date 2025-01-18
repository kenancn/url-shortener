from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url import URLCreate, URL
from app.services.url_service import URLService
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/shorten/", response_model=URL, status_code=201)
async def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    """Shortens a URL"""
    return await URLService.create_url(db, url)

@router.get("/{short_url}")
async def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    """Redirects from short URL to original URL"""
    url = await URLService.get_url(db, short_url)
    return RedirectResponse(url=str(url.original_url))

@router.get("/stats/{short_url}", response_model=URL)
async def get_url_stats(short_url: str, db: Session = Depends(get_db)):
    """Gets URL statistics"""
    return await URLService.get_url_stats(db, short_url) 