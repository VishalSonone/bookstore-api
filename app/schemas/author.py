from pydantic import BaseModel, Field, ConfigDict, constr, field_validator, EmailStr
from datetime import date, datetime
from enum import Enum
from typing import Optional
# --------------------
# Author Schemas
# --------------------
class AuthorBase(BaseModel):
    name: constr(min_length=2, max_length=100)
    bio: str | None = None
    birth_date: date | None = None
    nationality: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
