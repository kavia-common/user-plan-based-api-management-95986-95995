"""
Authentication, JWT utility functions, and dependency for current user using in-memory user store.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas

# In-memory user/plan store (No DB, no password hash for simplicity, do not use in production!)
USERS = [
    {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
        "password": "alicepw",
        "plan": "BASIC"
    },
    {
        "id": 2,
        "username": "bob",
        "email": "bob@example.com",
        "password": "bobpw",
        "plan": "PRO"
    },
    {
        "id": 3,
        "username": "carol",
        "email": "carol@example.com",
        "password": "carolpw",
        "plan": "ENTERPRISE"
    }
]

PLANS = [
    {"id": 1, "name": "BASIC", "description": "Basic plan, summary usage only."},
    {"id": 2, "name": "PRO", "description": "Pro plan, summary + analytics."},
    {"id": 3, "name": "ENTERPRISE", "description": "Full insights, downloads."},
]

username_to_user = {u["username"]: u for u in USERS}
id_to_user = {u["id"]: u for u in USERS}
plan_name_to_plan = {p["name"]: p for p in PLANS}
id_to_plan = {p["id"]: p for p in PLANS}

# PUBLIC_INTERFACE
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "supersecret_demo_key"  # No .env, just hardcoded for demo
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

def verify_password(plain_password, actual_password):
    # In demo, compare plain text (DO NOT USE IN REAL APP)
    return plain_password == actual_password

def get_password_hash(password):
    # Not real hash, placeholder for compability
    return password

# PUBLIC_INTERFACE
def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate user credentials against in-memory store."""
    user = username_to_user.get(username)
    if not user or not verify_password(password, user["password"]):
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
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
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

    user = username_to_user.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# PUBLIC_INTERFACE
def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Get user only if active (unused in-memory demo)."""
    return current_user
