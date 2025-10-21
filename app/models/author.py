from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String)
    birth_date = Column(Date)
    nationality = Column(String)

    # Relationships
    books = relationship("Book", back_populates="author",cascade="all, delete" )
