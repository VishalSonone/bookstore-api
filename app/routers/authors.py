from fastapi import APIRouter,HTTPException,status,Depends
from app.schemas.author import AuthorCreate,AuthorResponse,AuthorUpdate
from app.models.author import Author
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
router=APIRouter(
    prefix="/authors",
    tags=["Author"]
)

@router.post("/",response_model=AuthorResponse,status_code=status.HTTP_201_CREATED)
def create_author(author:AuthorCreate,db: Session= Depends(get_db)):
    new_author=Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/",response_model=List[AuthorResponse],status_code=status.HTTP_200_OK)
def get_all(db: Session=Depends(get_db)):
    authors=db.query(Author).all()
    if not authors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no authors registered")
    return authors

@router.get("/{id}",response_model=AuthorResponse,status_code=status.HTTP_200_OK)
def get_by_id(id:int,db:Session=Depends(get_db)):
    author=db.query(Author).filter(Author.id==id).one_or_none()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no author found with given id")
    return author

from fastapi import Response

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == id).one_or_none()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No author found with the given id"
        )
    db.delete(author)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@router.put("/{id}", response_model=AuthorResponse, status_code=status.HTTP_202_ACCEPTED)
def update_by_id(id: int, updated: AuthorCreate, db: Session = Depends(get_db)):
    dbAuthor = db.query(Author).filter(Author.id == id).one_or_none()
    if not dbAuthor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No author found with given id")

    # Full update
    dbAuthor.name = updated.name
    dbAuthor.bio = updated.bio
    dbAuthor.birth_date = updated.birth_date
    dbAuthor.nationality = updated.nationality

    db.commit()
    db.refresh(dbAuthor)
    return dbAuthor


@router.patch("/{id}", response_model=AuthorResponse, status_code=status.HTTP_202_ACCEPTED)
def partial_update_by_id(id: int, updated: AuthorUpdate, db: Session = Depends(get_db)):
    dbAuthor = db.query(Author).filter(Author.id == id).one_or_none()
    if not dbAuthor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No author found with given id")

    # Partial update: only update provided fields
    update_data = updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dbAuthor, key, value)

    db.commit()
    db.refresh(dbAuthor)
    return dbAuthor
