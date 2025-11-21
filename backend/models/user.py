"""
User domain models and schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(default="user", pattern="^(user|admin|researcher)$")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, pattern="^(user|admin|researcher)$")


class User(UserBase):
    """Full user domain model"""
    id: int
    created_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema (excludes sensitive data)"""
    id: int
    email: EmailStr
    name: str
    role: str
    is_active: bool
    created_at: str  # ISO format string
    
    class Config:
        from_attributes = True

