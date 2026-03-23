"""Authentication request and response schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr, Field, field_validator
from bson import ObjectId


class UserCreate(BaseModel):
    """Schema for user registration requests.
    
    Attributes:
        email: Valid email address
        username: Unique username (3-50 characters)
        password: Password (minimum 8 characters)
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema for user data in responses.
    
    Excludes sensitive fields like password/hashed_password.
    
    Attributes:
        id: User ID (converted from ObjectId to string)
        email: User email
        username: Username
        is_active: Whether account is active
        is_admin: Whether user has admin privileges
        created_at: Account creation timestamp
    """
    id: str
    email: str
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_object_id(cls, v: Any) -> str:
        """Convert ObjectId to string before validation."""
        if isinstance(v, ObjectId):
            return str(v)
        return str(v)


class LoginRequest(BaseModel):
    """Schema for login requests.
    
    Attributes:
        email: User email address
        password: User password
    """
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema for login responses.
    
    Attributes:
        message: Status message
    """
    message: str
