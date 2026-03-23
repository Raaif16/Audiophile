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
