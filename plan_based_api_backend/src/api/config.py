import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    """Config class for environment variables."""
    DATABASE_URL: str = Field(..., description="Database connection URL")
    JWT_SECRET_KEY: str = Field(..., description="Secret key for JWT signing")
    JWT_ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="JWT expiration in minutes")

def get_settings() -> Settings:
    """Load settings from environment variables."""
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
        JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
        ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)),
    )
