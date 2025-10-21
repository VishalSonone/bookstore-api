from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 1️⃣ Load environment variables from .env
load_dotenv()

# 2️⃣ Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# 3️⃣ Create SQLAlchemy engine
# connect_args needed only for SQLite; remove if using PostgreSQL
engine = create_engine(DATABASE_URL)

# 4️⃣ Create a session factory (for each request)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5️⃣ Create a base class for ORM models
Base = declarative_base()

# 6️⃣ Dependency function for FastAPI
def get_db():
    """Provides a DB session for each request and closes it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
