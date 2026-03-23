"""Authentication request and response schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


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
        id: User ID
        email: User email
        username: Username
        is_active: Whether account is active
        created_at: Account creation timestamp
    """
    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}


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
