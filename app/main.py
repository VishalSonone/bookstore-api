from fastapi import FastAPI
from app.database import engine, Base
from app.models import user, author, book, review
from app.routers import authors


app=FastAPI()
app.include_router(authors.router)

Base.metadata.create_all(bind=engine)



@app.get("/healthcheck")
def health_check():
    return {"Message":"OM NAMAH SHIVAY...."}