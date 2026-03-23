"""Admin router for admin-only endpoints."""

from fastapi import APIRouter, Depends
from typing import List

from app.dependencies import require_admin
from app.models import User
from app.schemas import UserResponse


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(admin: User = Depends(require_admin)):
    """Get all users (admin only).
    
    Args:
        admin: Current admin user from require_admin dependency
        
    Returns:
        List of all users
    """
    users = await User.find_all().to_list()
    return users


@router.get("/stats")
async def get_stats(admin: User = Depends(require_admin)):
    """Get application statistics (admin only).
    
    Args:
        admin: Current admin user from require_admin dependency
        
    Returns:
        Basic statistics about the application
    """
    total_users = await User.find_all().count()
    active_users = await User.find(User.is_active == True).count()
    admin_users = await User.find(User.is_admin == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users
    }