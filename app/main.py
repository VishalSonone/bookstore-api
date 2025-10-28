from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, author, book, review
from app.routers import authors,books,users,reviews


app=FastAPI()
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(reviews.router)



Base.metadata.create_all(bind=engine)



@app.get("/healthcheck")
def health_check():
    return {"Message":"BookStore Api is running..."}