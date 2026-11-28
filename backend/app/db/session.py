from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Determine active database engine
try:
    if settings.DATABASE_URL and not settings.DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        # Test connection
        with engine.connect() as conn:
            pass
        logger.info("Connected to primary PostgreSQL database.")
    else:
        raise ValueError("Using SQLite directly")
except Exception as e:
    if settings.USE_SQLITE_FALLBACK_IF_PG_UNAVAILABLE:
        logger.warning(f"PostgreSQL connection failed ({e}). Falling back to local SQLite database.")
        engine = create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False}
        )
    else:
        raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that provides a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
