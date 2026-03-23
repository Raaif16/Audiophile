"""Authentication router for user registration, login, and logout."""

from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.dependencies import get_current_user
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest
from app.services import hash_password, verify_password, create_access_token, DUMMY_HASH


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user.
    
    Args:
        user_data: User registration data (email, username, password)
        
    Returns:
        Created user data (without password)
        
    Raises:
        HTTPException: 400 if email or username already exists
    """
    # Check for duplicate email
    existing_email = await User.find_one(User.email == user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check for duplicate username
    existing_username = await User.find_one(User.username == user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user with hashed password
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    await user.insert()
    
    return user


@router.post("/login")
async def login(response: Response, login_data: LoginRequest):
    """Authenticate user and set access token cookie.
    
    Args:
        response: FastAPI Response object for setting cookies
        login_data: Login credentials (email, password)
        
    Returns:
        Success message
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    user = await User.find_one(User.email == login_data.email)
    
    # Verify password (use DUMMY_HASH if user not found for timing protection)
    if user:
        password_valid = verify_password(login_data.password, user.hashed_password)
    else:
        # Timing-safe comparison using dummy hash when user not found
        verify_password(login_data.password, DUMMY_HASH)
        password_valid = False
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create access token
    access_token = create_access_token(str(user.id))
    
    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    
    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    """Logout user and clear access token cookie.
    
    Args:
        response: FastAPI Response object for clearing cookies
        
    Returns:
        Success message
    """
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user.
    
    Args:
        current_user: Current user from JWT token cookie
        
    Returns:
        Current user data
    """
    return current_user
