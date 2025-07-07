import pytest
from unittest.mock import patch
from datetime import timedelta
from jose import jwt

from src.routes.auth.models import User, UserLogin
from src.routes.auth.operations import (
    create_user,
    get_user_by_username,
    authenticate_user,
    create_access_token,
    verify_token,
    get_current_user,
    pwd_context,
)


class TestAuthModels:
    """Test cases for authentication models."""

    def test_user_model_creation(self):
        """Test User model creation."""
        user = User(
            id=1, username="testuser", hashed_password="hashedpassword", role="user"
        )
        assert user.username == "testuser"
        assert user.hashed_password == "hashedpassword"
        assert user.role == "user"

    def test_user_login_model_creation(self):
        """Test UserLogin model creation."""
        user_login = UserLogin(username="testuser", password="plainpassword")
        assert user_login.username == "testuser"
        assert user_login.password == "plainpassword"


class TestAuthOperations:
    """Test cases for authentication operations."""

    def test_create_user(self, test_session):
        """Test user creation operation."""
        user_login = UserLogin(username="newuser", password="password123")
        result = create_user(user_login, test_session)

        assert result == "complete"

        # Verify user was created in database
        from sqlalchemy import text

        created_user = test_session.exec(
            text(f"SELECT * FROM user WHERE username = 'newuser'")
        ).first()
        assert created_user is not None

    def test_get_user_by_username_existing(self, test_session):
        """Test getting existing user by username."""
        # Create a test user first
        test_user = User(
            username="existinguser", hashed_password="hashedpass", role="user"
        )
        test_session.add(test_user)
        test_session.commit()

        # Test retrieval
        retrieved_user = get_user_by_username("existinguser", test_session)
        assert retrieved_user is not None
        assert retrieved_user.username == "existinguser"

    def test_get_user_by_username_nonexistent(self, test_session):
        """Test getting non-existent user by username."""
        retrieved_user = get_user_by_username("nonexistentuser", test_session)
        assert retrieved_user is None

    def test_authenticate_user_success(self, test_session):
        """Test successful user authentication."""
        # Create user with known password
        password = "testpassword"
        hashed_password = pwd_context.hash(password)

        test_user = User(
            username="authuser", hashed_password=hashed_password, role="user"
        )
        test_session.add(test_user)
        test_session.commit()

        # Test authentication
        authenticated_user = authenticate_user("authuser", password, test_session)
        assert authenticated_user is not False
        assert authenticated_user.username == "authuser"

    def test_authenticate_user_wrong_password(self, test_session):
        """Test authentication with wrong password."""
        # Create user
        hashed_password = pwd_context.hash("correctpassword")

        test_user = User(
            username="authuser2", hashed_password=hashed_password, role="user"
        )
        test_session.add(test_user)
        test_session.commit()

        # Test authentication with wrong password
        result = authenticate_user("authuser2", "wrongpassword", test_session)
        assert result is False

    def test_authenticate_user_nonexistent(self, test_session):
        """Test authentication with non-existent user."""
        result = authenticate_user("nonexistentuser", "anypassword", test_session)
        assert result is False

    @patch("src.routes.auth.operations.SECRET_KEY", "test_secret_key")
    @patch("src.routes.auth.operations.ALGORITHM", "HS256")
    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)

        # Decode token to verify contents
        decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
        assert decoded["sub"] == "testuser"
        assert decoded["role"] == "user"
        assert "exp" in decoded

    @patch("src.routes.auth.operations.SECRET_KEY", "test_secret_key")
    @patch("src.routes.auth.operations.ALGORITHM", "HS256")
    def test_create_access_token_with_expiry(self):
        """Test access token creation with custom expiry."""
        data = {"sub": "testuser", "role": "user"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta)

        # Decode token to verify contents
        decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
        assert decoded["sub"] == "testuser"
        assert "exp" in decoded

    @patch("src.routes.auth.operations.SECRET_KEY", "test_secret_key")
    @patch("src.routes.auth.operations.ALGORITHM", "HS256")
    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)

        payload = verify_token(token)
        assert payload["sub"] == "testuser"
        assert payload["role"] == "user"

    @patch("src.routes.auth.operations.SECRET_KEY", "test_secret_key")
    @patch("src.routes.auth.operations.ALGORITHM", "HS256")
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.here"

        with pytest.raises(Exception):  # Should raise HTTPException
            verify_token(invalid_token)

    @patch("src.routes.auth.operations.SECRET_KEY", "test_secret_key")
    @patch("src.routes.auth.operations.ALGORITHM", "HS256")
    def test_get_current_user(self):
        """Test getting current user from token."""
        data = {"sub": "testuser", "role": "admin"}
        token = create_access_token(data)

        username, role = get_current_user(token)
        assert username == "testuser"
        assert role == "admin"


class TestPasswordHashing:
    """Test cases for password hashing functionality."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "mysecretpassword"
        hashed = pwd_context.hash(password)

        # Hash should be different from original password
        assert hashed != password

        # Should be able to verify correct password
        assert pwd_context.verify(password, hashed) is True

        # Should fail with wrong password
        assert pwd_context.verify("wrongpassword", hashed) is False
