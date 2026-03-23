"""Authentication service with JWT token handling and Argon2 password hashing.

This module provides:
- JWT access token creation and decoding
- Password hashing using Argon2 via pwdlib
- Timing attack protection via dummy hash
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from pwdlib import PasswordHash

from app.config import get_settings


# Initialize password hasher with recommended settings (Argon2)
password_hash = PasswordHash.recommended()

# Dummy hash for timing attack protection when user not found
DUMMY_HASH = password_hash.hash("dummy")


def hash_password(password: str) -> str:
    """Hash a password using Argon2.
    
    Args:
        password: Plain text password
        
    Returns:
        Argon2 hash string
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash.
    
    Args:
        password: Plain text password to verify
        hashed: Argon2 hash to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return password_hash.verify(password, hashed)


def create_access_token(user_id: str) -> str:
    """Create a JWT access token for a user.
    
    Args:
        user_id: The user's ID to encode in the token
        
    Returns:
        JWT token string
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": now,
        "type": "access"
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    settings = get_settings()
    
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )
