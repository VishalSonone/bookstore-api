from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
    published_date = Column(Date)
    isbn = Column(String, unique=True)
    price = Column(Float)
    stock = Column(Integer)
    cover_image_url = Column(String)

    # Relationships
    author = relationship("Author", back_populates="books")
    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete"   
    )
