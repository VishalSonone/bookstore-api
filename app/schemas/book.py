from pydantic import BaseModel, Field, ConfigDict, constr, field_validator, EmailStr
from datetime import date
from .author import AuthorResponse
class BookBase(BaseModel):
    title: constr(min_length=2, max_length=100)
    author_id: int
    published_date: date | None = None
    isbn: constr(min_length=10, max_length=13)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    cover_image_url: str | None = None

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("ISBN must contain only digits")
        return v

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookDetailResponse(BookResponse):
    author: AuthorResponse   # nested author details
