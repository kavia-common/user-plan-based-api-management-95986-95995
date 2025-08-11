"""
Pydantic schemas for users, plans, and authentication.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# User-related schemas

class UserBase(BaseModel):
    username: str = Field(..., description="Username for the user.")
    email: EmailStr = Field(..., description="User email address.")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User password (min 6 chars).")

class UserRead(UserBase):
    id: int = Field(..., description="ID of the user.")
    plan: Optional[str] = Field(None, description="Name of the plan assigned to user.")

    class Config:
        orm_mode = True

# Plan-related schemas

class PlanBase(BaseModel):
    name: str = Field(..., description="Name of the plan.")
    description: Optional[str] = Field(None, description="Description for the plan.")

class PlanCreate(PlanBase):
    pass

class PlanRead(PlanBase):
    id: int = Field(..., description="Plan ID")
    class Config:
        orm_mode = True

# Auth/JWT schemas

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Assignment schema

class PlanAssignment(BaseModel):
    user_id: int
    plan_id: int
