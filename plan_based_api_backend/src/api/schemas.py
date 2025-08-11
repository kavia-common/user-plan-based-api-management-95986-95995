from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Payload for user registration."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Payload for user login."""
    username: str
    password: str

class UserResponse(BaseModel):
    """User response model."""
    id: int
    username: str
    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class PlanCreate(BaseModel):
    """Payload for creating/updating a plan."""
    name: str = Field(..., description="Plan name")
    description: Optional[str] = Field(None, description="Description")

class PlanResponse(BaseModel):
    """Plan response model."""
    id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True

class AssignPlanRequest(BaseModel):
    """Payload to assign a plan to a user."""
    username: str
    plan_name: str

class Token(BaseModel):
    """Returned JWT token structure."""
    access_token: str
    token_type: str = "bearer"
