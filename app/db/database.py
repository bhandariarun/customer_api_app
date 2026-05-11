"""
database.py — The Connection Layer
Sets up the SQLAlchemy engine and session factory.
Reads all credentials from environment variables (loaded from .env).

Twelve-Factor App:
  Factor III  – Config in the environment, never hard-coded.
  Factor IV   – DB is a backing service; swap it by changing DATABASE_URL only.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.logger.logger import get_logger

# Load .env file from the project root (two levels up from this file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

logger = get_logger(__name__)

def build_database_url() -> str:
    """Construct the database URL from environment variables."""
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

DATABASE_URL = build_database_url()

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    # Verify the connection is reachable at startup
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Database connection established successfully.")
except Exception as exc:
    logger.error("Failed to connect to the database: %s", exc)
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Yields a database session and guarantees it is closed afterwards.
    Use as a FastAPI dependency:  db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed.")
