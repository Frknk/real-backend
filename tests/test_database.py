import pytest
from sqlmodel import Session
from src.database import init_db, get_session
from src.routes.auth.models import User


class TestDatabase:
    """Test cases for database functionality."""

    def test_init_db(self, test_db):
        """Test database initialization."""
        # init_db should create all tables without error
        init_db()
        # If we get here without exception, init_db worked
        assert True

    def test_get_session_generator(self, test_db):
        """Test that get_session returns a valid session generator."""
        session_gen = get_session()
        session = next(session_gen)
        assert isinstance(session, Session)

        # Test that we can use the session
        from sqlmodel import select

        users = session.exec(select(User)).all()
        assert isinstance(users, list)

    def test_database_crud_operations(self, test_session):
        """Test basic CRUD operations on the database."""
        # Create a test user
        test_user = User(username="dbtest", hashed_password="hashed123", role="user")

        # Create
        test_session.add(test_user)
        test_session.commit()
        test_session.refresh(test_user)

        assert test_user.id is not None

        # Read
        retrieved_user = test_session.get(User, test_user.id)
        assert retrieved_user is not None
        assert retrieved_user.username == "dbtest"

        # Update
        retrieved_user.role = "admin"
        test_session.add(retrieved_user)
        test_session.commit()

        updated_user = test_session.get(User, test_user.id)
        assert updated_user.role == "admin"

        # Delete
        test_session.delete(updated_user)
        test_session.commit()

        deleted_user = test_session.get(User, test_user.id)
        assert deleted_user is None
