from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.review import Review
from app.models.user import User
from app.models.book import Book
from app.schemas.review import ReviewCreate, ReviewResponse,ReviewUpdate
from typing import List
from fastapi import Response
router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == review.user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the given ID"
        )
    book = db.query(Book).filter(Book.id == review.book_id).one_or_none()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with the given ID"
        )
    existing_review = (
        db.query(Review)
        .filter(Review.book_id == review.book_id, Review.user_id == review.user_id)
        .first()
    )
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already reviewed this book"
        )
    new_review = Review(**review.model_dump())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/", response_model=List[ReviewResponse], status_code=status.HTTP_200_OK)
def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).all()
    return reviews

@router.get("/{id}", response_model=ReviewResponse, status_code=status.HTTP_200_OK)
def get_review_by_id(id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == id).one_or_none()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found with the given ID"
        )
    return review

@router.get("/book/{book_id}", response_model=List[ReviewResponse], status_code=status.HTTP_200_OK)
def get_reviews_by_book(book_id: int, db: Session = Depends(get_db)):
    # Check if book exists
    book = db.query(Book).filter(Book.id == book_id).one_or_none()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with the given ID"
        )

    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return reviews

@router.get("/user/{user_id}", response_model=List[ReviewResponse], status_code=status.HTTP_200_OK)
def get_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the given ID"
        )

    reviews = db.query(Review).filter(Review.user_id == user_id).all()
    return reviews
@router.put("/{id}", response_model=ReviewResponse, status_code=status.HTTP_200_OK)
def update_review(id: int, updated: ReviewCreate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == id).one_or_none()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found with the given ID"
        )

    # Ensure the user exists
    user = db.query(User).filter(User.id == updated.user_id).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with the given ID"
        )

    # Ensure the book exists
    book = db.query(Book).filter(Book.id == updated.book_id).one_or_none()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with the given ID"
        )

    # Update all fields
    for key, value in updated.model_dump().items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@router.patch("/{id}", response_model=ReviewResponse, status_code=status.HTTP_200_OK)
def partial_update_review(id: int, updated: ReviewUpdate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == id).one_or_none()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found with the given ID"
        )

    update_data = updated.model_dump(exclude_unset=True)

    # Validate new user/book if provided
    if "user_id" in update_data:
        user = db.query(User).filter(User.id == update_data["user_id"]).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with the given ID"
            )

    if "book_id" in update_data:
        book = db.query(Book).filter(Book.id == update_data["book_id"]).one_or_none()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found with the given ID"
            )

    for key, value in update_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == id).one_or_none()
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found with the given ID"
        )

    db.delete(db_review)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)