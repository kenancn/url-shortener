from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import url
from app.core.database import engine, Base
import logging

# Logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener Service",
    description="""
    URL Shortener API allows you to shorten long URLs and manage them.
    
    ## Features
    * URL Shortening
    * Redirection
    * Statistics Tracking
    """,
    version="1.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add router
app.include_router(url.router, tags=["urls"])

@app.get("/")
async def root():
    return {"message": "Welcome to URL Shortener API"} 