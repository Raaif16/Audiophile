"""FastAPI dependencies for dependency injection.

This module provides reusable dependencies for FastAPI's Depends() system,
particularly for authentication and authorization.
"""

from fastapi import Request, HTTPException, status, Depends

from app.models import User
from app.services import decode_token


async def get_current_user(request: Request) -> User:
    """Get the current authenticated user from JWT token cookie.
    
    Extracts access_token from httpOnly cookie, validates JWT signature
    and expiration, then fetches the user from the database.
    
    Args:
        request: The FastAPI Request object
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    # Extract token from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        # Decode and validate token
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Fetch user from database
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


async def require_user(current_user: User = Depends(get_current_user)) -> User:
    """Require authenticated user (wrapper for clarity).
    
    This is an alias for get_current_user that makes route definitions
    more readable when authentication is required.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        Authenticated User object
    """
    return current_user
