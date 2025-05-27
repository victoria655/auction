# models/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the database connection URL
DATABASE_URL = "sqlite:///auction.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Preferred session factory for clean session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Backward-compatible global session (not recommended for new code)
session = SessionLocal()

# Base class for models
Base = declarative_base()
