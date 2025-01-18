from pydantic import BaseModel, HttpUrl, computed_field, ConfigDict
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    """Base URL schema"""
    original_url: HttpUrl

class URLCreate(URLBase):
    """Schema for URL creation"""
    model_config = ConfigDict(from_attributes=True)

class URL(URLBase):
    """Schema for URL response"""
    id: int
    short_url: str
    clicks: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @computed_field
    def full_url(self) -> str:
        """Computes full URL with domain"""
        return f"http://localhost:8000/{self.short_url}"

    model_config = ConfigDict(from_attributes=True) 