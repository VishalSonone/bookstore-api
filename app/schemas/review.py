from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


# Base schema for shared fields
class ReviewBase(BaseModel):
    rating: Optional[int] = Field(
        None, ge=1, le=5, description="Rating must be between 1 and 5"
    )
    comment: Optional[str] = Field(
        None, max_length=500, description="Optional review comment"
    )


# Schema for creating a review
class ReviewCreate(ReviewBase):
    book_id: int
    user_id: int


# Schema for partial updates (PATCH)
class ReviewUpdate(ReviewBase):
    book_id: Optional[int] = None
    user_id: Optional[int] = None


# Schema for responses
class ReviewResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
