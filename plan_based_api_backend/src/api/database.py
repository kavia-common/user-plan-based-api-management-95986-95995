from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# PUBLIC_INTERFACE
def get_db():
    """Yield a new database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
