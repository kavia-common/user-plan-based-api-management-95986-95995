"""
Authentication, JWT utility functions, and dependency for current user.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, database, schemas

# PUBLIC_INTERFACE
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = database.get_env("PLAN_API_SECRET_KEY", "default_supersecret_key")  # Should be set in .env!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours

def verify_password(plain_password, hashed_password):
    return models.User.verify_password(models.User, plain_password, hashed_password)

def get_password_hash(password):
    return models.User.get_password_hash(password)

# PUBLIC_INTERFACE
def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """Authenticate user credentials against database."""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not user.verify_password(password):
        return None
    return user

# PUBLIC_INTERFACE
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token (default expiry)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# PUBLIC_INTERFACE
def get_db():
    """FastAPI dependency for DB session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Get the current user based on JWT access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please login.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# PUBLIC_INTERFACE
def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Get user only if active (place-holder for further checks)."""
    # Could add is_active, is_superuser etc later
    return current_user
