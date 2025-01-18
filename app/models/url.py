from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class URL(Base):
    """URL model for storing shortened URLs"""
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    
    # Traffic Metrics
    clicks = Column(Integer, default=0)
    avg_response_time = Column(Float, default=0.0)
    last_accessed = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 