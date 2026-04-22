"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,  # Enable reconnection on stale connections
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Max number of connections beyond pool_size
    pool_timeout=30,  # Timeout for getting connection from pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

# Create sessionmaker factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI endpoints.

    This function creates a new database session for each request
    and ensures it's closed after the request is processed.

    Yields:
        SQLAlchemy Session: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection():
    """
    Check if the database connection is working.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False
