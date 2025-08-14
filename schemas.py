from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
import re

class ReviewBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    text: str = Field(..., min_length=10, max_length=1000, description="Review text")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")

class ReviewCreate(ReviewBase):
    pass 

class ReviewOut(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Contact name")
    email: EmailStr = Field(..., description="Valid email address")
    message: str = Field(..., min_length=10, max_length=2000, description="Message content")
    company: Optional[str] = Field("", max_length=0, description="Honeypot field (hidden)")  # Honeypot field (hidden in frontend)
    
    @validator('name')
    def validate_name(cls, v):
        # Remove extra whitespace and check for valid characters
        cleaned = re.sub(r'\s+', ' ', v.strip())
        if not re.match(r'^[a-zA-Z\s\-\'\.]+$', cleaned):
            raise ValueError('Name contains invalid characters')
        return cleaned
    
    @validator('message')
    def validate_message(cls, v):
        # Remove excessive whitespace and check for reasonable content
        cleaned = re.sub(r'\s+', ' ', v.strip())
        if len(cleaned) < 10:
            raise ValueError('Message must be at least 10 characters long')
        if len(cleaned) > 2000:
            raise ValueError('Message cannot exceed 2000 characters')
        return cleaned