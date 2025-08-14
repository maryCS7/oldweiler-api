from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base 

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())