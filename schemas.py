from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ReviewBase(BaseModel):
    name: str
    text: str
    rating: Optional[int] = None

class ReviewCreate(ReviewBase):
    pass 

class ReviewOut(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ContactForm(BaseModel):
    name: str
    email: str
    message: str
    company: Optional[str] = ""  # Honeypot field (hidden in frontend)