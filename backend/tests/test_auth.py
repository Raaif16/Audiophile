"""Tests for authentication service."""

import pytest
from datetime import datetime, timezone, timedelta
from app.services.auth_service import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
    DUMMY_HASH,
)


class TestTokenCreation:
    """Tests for JWT token creation and decoding."""
    
    def test_create_access_token(self):
        """Test that create_access_token creates a valid token with exp claim."""
        user_id = "user123"
        token = create_access_token(user_id)
        
        # Token should be a non-empty string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode and verify claims
        payload = decode_token(token)
        assert payload["sub"] == user_id
        assert "exp" in payload
        
        # Verify expiration is approximately 30 minutes from now
        exp_timestamp = payload["exp"]
        now_timestamp = int(datetime.now(timezone.utc).timestamp())
        expected_exp = now_timestamp + 30 * 60  # 30 minutes in seconds
        
        # Allow 10 seconds tolerance for test execution time
        assert abs(exp_timestamp - expected_exp) < 10
    
    def test_decode_valid_token(self):
        """Test that decode_token returns correct payload for valid token."""
        user_id = "test_user_456"
        token = create_access_token(user_id)
        
        payload = decode_token(token)
        
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_decode_expired_token(self):
        """Test that decode_token raises exception for expired token."""
        import jwt
        from app.config import get_settings
        
        settings = get_settings()
        
        # Create a token that expired 1 hour ago
        expired_time = datetime.now(timezone.utc) - timedelta(hours=1)
        payload = {
            "sub": "test_user",
            "exp": expired_time,
        }
        expired_token = jwt.encode(
            payload,
            settings.secret_key,
            algorithm=settings.algorithm,
        )
        
        # Should raise an exception for expired token
        with pytest.raises(Exception):
            decode_token(expired_token)


class TestPasswordHashing:
    """Tests for password hashing and verification."""
    
    def test_hash_password(self):
        """Test that hash_password produces different hashes for same password."""
        password = "my_secret_password"
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Both should be strings
        assert isinstance(hash1, str)
        assert isinstance(hash2, str)
        
        # Hashes should be different due to salting
        assert hash1 != hash2
        
        # Both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct password."""
        password = "correct_horse_battery_staple"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_wrong(self):
        """Test that verify_password returns False for wrong password."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_dummy_hash_exists_and_verifies(self):
        """Test that DUMMY_HASH exists for timing attack protection."""
        # DUMMY_HASH should exist and be a string
        assert isinstance(DUMMY_HASH, str)
        assert len(DUMMY_HASH) > 0
        
        # DUMMY_HASH should verify against "dummy" password
        assert verify_password("dummy", DUMMY_HASH) is True
        
        # DUMMY_HASH should NOT verify against other passwords
        assert verify_password("wrong", DUMMY_HASH) is False
