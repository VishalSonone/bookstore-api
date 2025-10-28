from fastapi import APIRouter,HTTPException,Depends,status, Query
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate,BookResponse,BookDetailResponse
from app.database import get_db
from typing import List
from typing import Optional
router=APIRouter(
    prefix="/books",
    tags=["Book"]
)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_author = db.query(Author).filter(Author.id == book.author_id).one_or_none()
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author does not exist with the given id"
        )

    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/",response_model=List[BookResponse],status_code=status.HTTP_200_OK)
def get_all(db:Session=Depends(get_db)):
    books=db.query(Book).all()
    return books

@router.get("/{id}",response_model=BookDetailResponse,status_code=status.HTTP_200_OK)
def get_by_id(id:int,db:Session=Depends(get_db)):
    dbBook=db.query(Book).filter(Book.id==id).one_or_none()
    if not dbBook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found with given id")
    return dbBook
@router.put("/{id}", response_model=BookDetailResponse, status_code=status.HTTP_200_OK)
def update_book(id: int, updated: BookCreate, db: Session = Depends(get_db)):
    dbBook = db.query(Book).filter(Book.id == id).one_or_none()
    if not dbBook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with given id"
        )
    
    # Check author exists
    dbAuthor = db.query(Author).filter(Author.id == updated.author_id).one_or_none()
    if not dbAuthor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found with given id"
        )

    # Update all fields
    dbBook.title = updated.title
    dbBook.author_id = updated.author_id
    dbBook.cover_image_url = updated.cover_image_url
    dbBook.isbn = updated.isbn
    dbBook.price = updated.price
    dbBook.published_date = updated.published_date
    dbBook.stock = updated.stock

    db.commit()
    db.refresh(dbBook)
    return dbBook


@router.delete("/{id}",response_model=BookResponse,status_code=status.HTTP_200_OK)
def delete_by_id(id:int,db:Session=Depends(get_db)):
    dbBook=db.query(Book).filter(Book.id==id).one_or_none()
    if not dbBook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found with given id"
        )
    db.delete(dbBook)
    db.commit()
    return dbBook

@router.get("/author/{id}", response_model=List[BookDetailResponse], status_code=status.HTTP_200_OK)
def get_by_author(id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == id).one_or_none()
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found with given id"
        )

    dbBooks = db.query(Book).filter(Book.author_id == id).all()
    return dbBooks  
@router.get("/search", response_model=List[BookDetailResponse], status_code=status.HTTP_200_OK)
def search_books(
    title: Optional[str] = Query(None, description="Search by book title"),
    isbn: Optional[str] = Query(None, description="Search by ISBN"),
    author_name: Optional[str] = Query(None, description="Search by author name"),
    db: Session = Depends(get_db)
):
    query = db.query(Book).join(Author)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if isbn:
        query = query.filter(Book.isbn.ilike(f"%{isbn}%"))
    if author_name:
        query = query.filter(Author.name.ilike(f"%{author_name}%"))

    results = query.all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books found matching the criteria"
        )

    return results