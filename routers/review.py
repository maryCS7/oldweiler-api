from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Review
from schemas import ReviewCreate, ReviewOut
from database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

# GET all reviews
@router.get("/", response_model=list[ReviewOut])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).order_by(Review.created_at.desc()).all()

# POST a new review
@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    print("Received review:", review)
    try:
        new_review = Review(**review.dict())
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except Exception as e:
        print("Error creating review:", e)
        raise HTTPException(status_code=500, detail=str(e))
    