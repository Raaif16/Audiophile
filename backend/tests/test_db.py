"""Database connection tests."""

import pytest
import os
from datetime import datetime

from app.models import User


# Check if MongoDB is available (skip connection tests if not)
mongodb_available = os.environ.get("MONGODB_URL") is not None or os.path.exists("/tmp/mongodb-available")


class TestDatabaseConnection:
    """Tests for database initialization and connection."""
    
    @pytest.mark.skipif(not mongodb_available, reason="MongoDB not available in test environment")
    @pytest.mark.asyncio
    async def test_init_db_creates_client(self):
        """Test that init_db() creates a database client."""
        from app.database import init_db, close_db, client as db_client
        
        await init_db()
        assert db_client is not None
        await close_db()


class TestUserModel:
    """Tests for User document model."""
    
    def test_user_has_correct_fields(self):
        """Test that User model has all required fields."""
        # Check field existence by inspecting model fields
        fields = User.model_fields
        
        assert "email" in fields
        assert "username" in fields
        assert "hashed_password" in fields
        assert "is_active" in fields
        assert "is_admin" in fields
        assert "created_at" in fields
    
    def test_user_default_values(self):
        """Test that User model has correct default values."""
        fields = User.model_fields
        
        # Check defaults
        is_active_default = fields["is_active"].default
        is_admin_default = fields["is_admin"].default
        
        assert is_active_default == True
        assert is_admin_default == False
    
    def test_user_collection_name(self):
        """Test that User uses correct collection name."""
        assert User.Settings.name == "users"
    
    def test_user_field_types(self):
        """Test that User fields have correct types/indexes."""
        # Email field should be Indexed with unique constraint
        email_annotation = User.model_fields["email"].annotation
        # The Indexed type wraps the actual type
        assert "Indexed" in str(email_annotation)
        
        # Username field should be Indexed with unique constraint
        username_annotation = User.model_fields["username"].annotation
        assert "Indexed" in str(username_annotation)
