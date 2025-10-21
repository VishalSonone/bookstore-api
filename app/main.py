from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, author, book, review
from app.routers import authors,books


app=FastAPI()
app.include_router(authors.router)
app.include_router(books.router)

Base.metadata.create_all(bind=engine)



@app.get("/healthcheck")
def health_check():
    return {"Message":"BookStore Api is running..."}