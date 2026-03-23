"""Tests for authentication endpoints and schemas."""

import pytest
import uuid
from datetime import datetime

from app.schemas.auth import UserCreate, UserResponse, LoginRequest


def get_unique_email():
    """Generate a unique email for testing."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def get_unique_username():
    """Generate a unique username for testing."""
    return f"user_{uuid.uuid4().hex[:8]}"


class TestUserCreate:
    """Tests for UserCreate schema."""
    
    def test_user_create_valid(self):
        """Test that valid user data is accepted."""
        user = UserCreate(
            email="test@example.com",
            username="testuser",
            password="securepassword123"
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.password == "securepassword123"
    
    def test_user_create_invalid_email(self):
        """Test that invalid email is rejected."""
        with pytest.raises(ValueError):
            UserCreate(
                email="not-an-email",
                username="testuser",
                password="securepassword123"
            )
    
    def test_user_create_short_username(self):
        """Test that username below min length is rejected."""
        with pytest.raises(ValueError):
            UserCreate(
                email="test@example.com",
                username="ab",  # Too short
                password="securepassword123"
            )
    
    def test_user_create_short_password(self):
        """Test that password below min length is rejected."""
        with pytest.raises(ValueError):
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="short"  # Too short
            )


class TestUserResponse:
    """Tests for UserResponse schema."""
    
    def test_user_response_has_no_password(self):
        """Test that UserResponse does not include password field."""
        # Check that password is not in the model fields
        assert "password" not in UserResponse.model_fields
        assert "hashed_password" not in UserResponse.model_fields
    
    def test_user_response_structure(self):
        """Test that UserResponse has expected fields."""
        expected_fields = {"id", "email", "username", "is_active", "created_at"}
        actual_fields = set(UserResponse.model_fields.keys())
        assert expected_fields <= actual_fields


class TestLoginRequest:
    """Tests for LoginRequest schema."""
    
    def test_login_request_valid(self):
        """Test that valid login data is accepted."""
        login = LoginRequest(
            email="test@example.com",
            password="password123"
        )
        assert login.email == "test@example.com"
        assert login.password == "password123"
    
    def test_login_request_invalid_email(self):
        """Test that invalid email is rejected."""
        with pytest.raises(ValueError):
            LoginRequest(
                email="not-an-email",
                password="password123"
            )


@pytest.mark.asyncio
class TestAuthRouter:
    """Tests for authentication router endpoints."""
    
    async def test_register_success(self, client):
        """Test successful user registration."""
        response = await client.post(
            "/auth/register",
            json={
                "email": get_unique_email(),
                "username": get_unique_username(),
                "password": "securepassword123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data
    
    async def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        email = get_unique_email()
        # First registration
        await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": get_unique_username(),
                "password": "securepassword123"
            }
        )
        # Second registration with same email
        response = await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": get_unique_username(),
                "password": "securepassword123"
            }
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()
    
    async def test_register_duplicate_username(self, client):
        """Test registration with duplicate username fails."""
        username = get_unique_username()
        # First registration
        await client.post(
            "/auth/register",
            json={
                "email": get_unique_email(),
                "username": username,
                "password": "securepassword123"
            }
        )
        # Second registration with same username
        response = await client.post(
            "/auth/register",
            json={
                "email": get_unique_email(),
                "username": username,
                "password": "securepassword123"
            }
        )
        assert response.status_code == 400
        assert "username" in response.json()["detail"].lower()
    
    async def test_login_success(self, client):
        """Test successful login sets httpOnly cookie."""
        email = get_unique_email()
        password = "securepassword123"
        
        # Register a user first
        await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": get_unique_username(),
                "password": password
            }
        )
        
        # Login
        response = await client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"
        
        # Check for httpOnly cookie
        cookies = response.cookies
        assert "access_token" in cookies
    
    async def test_login_invalid_credentials(self, client):
        """Test login with wrong password fails."""
        email = get_unique_email()
        
        # Register a user first
        await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": get_unique_username(),
                "password": "securepassword123"
            }
        )
        
        # Login with wrong password
        response = await client.post(
            "/auth/login",
            json={
                "email": email,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
    
    async def test_login_nonexistent_user(self, client):
        """Test login with non-existent user fails."""
        response = await client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401


@pytest.mark.asyncio
class TestLogout:
    """Tests for logout endpoint."""
    
    async def test_logout_clears_cookie(self, client):
        """Test that logout clears the access_token cookie."""
        email = get_unique_email()
        password = "securepassword123"
        
        # Register and login first
        await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": get_unique_username(),
                "password": password
            }
        )
        
        login_response = await client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert "access_token" in login_response.cookies
        
        # Logout
        logout_response = await client.post("/auth/logout")
        assert logout_response.status_code == 200
        assert logout_response.json()["message"] == "Logout successful"


@pytest.mark.asyncio
class TestGetMe:
    """Tests for /auth/me endpoint."""
    
    async def test_get_me_authenticated(self, client):
        """Test that /me returns user data when authenticated."""
        email = get_unique_email()
        username = get_unique_username()
        password = "securepassword123"
        
        # Register user
        await client.post(
            "/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password
            }
        )
        
        # Login to get cookie
        await client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        
        # Get current user
        me_response = await client.get("/auth/me")
        assert me_response.status_code == 200
        data = me_response.json()
        assert data["email"] == email
        assert data["username"] == username
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data
    
    async def test_get_me_unauthenticated(self, client):
        """Test that /me returns 401 when not authenticated."""
        response = await client.get("/auth/me")
        assert response.status_code == 401
