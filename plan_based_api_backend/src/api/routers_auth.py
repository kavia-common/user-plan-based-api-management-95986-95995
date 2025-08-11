from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, models, auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# PUBLIC_INTERFACE
@router.post("/register", summary="Register a new user", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a user with username and password."""
    existing_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user_data.password)
    user = models.User(username=user_data.username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# PUBLIC_INTERFACE
@router.post("/login", summary="User login", response_model=schemas.Token)
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = auth.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = auth.create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=token)
