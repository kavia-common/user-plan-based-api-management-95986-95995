"""
Database setup and session management for plan-based API backend.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# PUBLIC_INTERFACE
def get_env(key: str, default: str = None) -> str:
    """Get environment variable from .env, loading if needed."""
    # Only call once per process
    load_dotenv()
    val = os.getenv(key)
    if val is None and default is not None:
        return default
    if val is None:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return val

DB_URL = get_env("PLAN_API_DB_URL", "sqlite:///./planapi.sqlite3")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
