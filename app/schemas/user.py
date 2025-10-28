from pydantic import BaseModel, Field, ConfigDict, constr, field_validator, EmailStr
from datetime import date, datetime
from enum import Enum
from typing import Optional


class Role(str, Enum):
    admin = "admin"
    user = "user"


class UserBase(BaseModel):
    username: constr(min_length=3, max_length=30, pattern="^[A-Za-z0-9_]+$") = Field(
        ..., description="Username must be 3–30 chars, letters/numbers/underscores only"
    )
    email: EmailStr


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=50) = Field(
        ..., description="Password must be at least 6 characters long"
    )
    role: Role = Role.user


class UserResponse(UserBase):
    id: int
    role: Role

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None
