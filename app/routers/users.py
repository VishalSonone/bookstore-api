from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users



@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, updated: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    if db.query(User).filter(User.username == updated.username, User.id != id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already in use")

    if db.query(User).filter(User.email == updated.email, User.id != id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    for field, value in updated.model_dump().items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user



@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def partial_update_user(id: int, updated: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = updated.model_dump(exclude_unset=True)


    if "username" in update_data:
        if db.query(User).filter(User.username == update_data["username"], User.id != id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already in use")

    if "email" in update_data:
        if db.query(User).filter(User.email == update_data["email"], User.id != id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).one_or_none()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
