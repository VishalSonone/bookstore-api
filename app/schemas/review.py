from pydantic import BaseModel, Field, ConfigDict, constr, field_validator, EmailStr


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None

class ReviewCreate(ReviewBase):
    book_id: int
    user_id: int

class ReviewResponse(ReviewBase):
    id: int
    book_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

