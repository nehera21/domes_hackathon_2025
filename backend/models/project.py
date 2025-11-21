"""
Project domain models and schemas.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project model with common fields"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: str = Field(default="active", pattern="^(active|completed|archived)$")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    owner_id: int


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(active|completed|archived)$")


class Project(ProjectBase):
    """Full project domain model"""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    """Project response schema"""
    id: int
    name: str
    description: Optional[str]
    status: str
    owner_id: int
    owner_name: Optional[str] = None  # Name of the project owner
    created_at: str  # ISO format string
    updated_at: str  # ISO format string
    
    class Config:
        from_attributes = True

