import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
import tempfile
import os
from unittest.mock import patch

from src.app import create_app
from src.database import get_session


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db():
    """Create a test database using SQLite in memory."""
    # Create a temporary database file
    temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_db.close()

    # Create SQLite connection string
    database_url = f"sqlite:///{temp_db.name}"

    # Create test engine with SQLite
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    yield engine

    # Cleanup
    engine.dispose()
    os.unlink(temp_db.name)


@pytest.fixture
def test_session(test_db):
    """Create a test database session."""
    with Session(test_db) as session:
        yield session


@pytest.fixture
def client(test_session):
    """Create a test client with dependency override."""

    def get_test_session():
        yield test_session

    # Mock environment variables for testing
    with patch.dict(
        os.environ,
        {
            "SECRET_KEY": "test_secret_key_for_testing_only",
            "ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
            "ALLOWED_ORIGIN": "http://localhost:3000",
            "DB_URL": "sqlite:///test.db",  # This will be overridden by test_db fixture
        },
    ):
        app = create_app()
        app.dependency_overrides[get_session] = get_test_session

        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {"username": "testuser", "password": "testpassword123"}


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "description": "A test product description",
        "stock": 10,
        "price": 99.99,
        "provider_name": "Test Provider",
        "category_name": "Test Category",
        "brand_name": "Test Brand",
    }


@pytest.fixture
def sample_category_data():
    """Sample category data for testing."""
    return {"name": "Test Category", "description": "A test category description"}


@pytest.fixture
def sample_brand_data():
    """Sample brand data for testing."""
    return {"name": "Test Brand", "description": "A test brand description"}


@pytest.fixture
def sample_provider_data():
    """Sample provider data for testing."""
    return {
        "ruc": 123456789,
        "name": "Test Provider",
        "address": "123 Test Street",
        "phone": "555-1234",
        "email": "test@provider.com",
    }


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return {
        "dni": 12345678,
        "name": "Test",
        "last_name": "Customer",
        "email": "test@customer.com",
    }


@pytest.fixture
def authenticated_headers(client, sample_user_data):
    """Get authentication headers for testing protected endpoints."""
    # Register user
    client.post("/auth/register", json=sample_user_data)

    # Login and get token
    response = client.post(
        "/auth/token",
        data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        },
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
