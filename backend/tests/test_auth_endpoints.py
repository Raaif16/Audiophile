"""Tests for authentication endpoints and schemas."""

import pytest
from datetime import datetime

from app.schemas.auth import UserCreate, UserResponse, LoginRequest


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
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data
    
    async def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        # First registration
        await client.post(
            "/auth/register",
            json={
                "email": "dup@example.com",
                "username": "user1",
                "password": "securepassword123"
            }
        )
        # Second registration with same email
        response = await client.post(
            "/auth/register",
            json={
                "email": "dup@example.com",
                "username": "user2",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()
    
    async def test_register_duplicate_username(self, client):
        """Test registration with duplicate username fails."""
        # First registration
        await client.post(
            "/auth/register",
            json={
                "email": "user1@example.com",
                "username": "dupuser",
                "password": "securepassword123"
            }
        )
        # Second registration with same username
        response = await client.post(
            "/auth/register",
            json={
                "email": "user2@example.com",
                "username": "dupuser",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 400
        assert "username" in response.json()["detail"].lower()
    
    async def test_login_success(self, client):
        """Test successful login sets httpOnly cookie."""
        # Register a user first
        await client.post(
            "/auth/register",
            json={
                "email": "login@example.com",
                "username": "loginuser",
                "password": "securepassword123"
            }
        )
        
        # Login
        response = await client.post(
            "/auth/login",
            json={
                "email": "login@example.com",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"
        
        # Check for httpOnly cookie
        cookies = response.cookies
        assert "access_token" in cookies
    
    async def test_login_invalid_credentials(self, client):
        """Test login with wrong password fails."""
        # Register a user first
        await client.post(
            "/auth/register",
            json={
                "email": "badlogin@example.com",
                "username": "badloginuser",
                "password": "securepassword123"
            }
        )
        
        # Login with wrong password
        response = await client.post(
            "/auth/login",
            json={
                "email": "badlogin@example.com",
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
