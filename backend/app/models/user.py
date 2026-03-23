from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """User document model for MongoDB with Beanie ODM.
    
    Attributes:
        email: Unique email address (indexed)
        username: Unique username (indexed)
        hashed_password: Argon2 hashed password
        is_active: Whether the account is active
        is_admin: Whether the user has admin privileges
        created_at: Account creation timestamp
    """
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        """Beanie settings for the User document."""
        name = "users"
