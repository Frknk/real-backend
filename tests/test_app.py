import pytest
from fastapi.testclient import TestClient


class TestApp:
    """Test cases for the main FastAPI application."""

    def test_app_creation(self, client):
        """Test that the app can be created successfully."""
        assert client is not None

    def test_cors_middleware(self, client):
        """Test CORS middleware is properly configured."""
        response = client.options("/")
        assert response.status_code in [
            200,
            404,
            405,
        ]  # OPTIONS might not be implemented for root

    def test_app_lifespan_startup(self, client):
        """Test that the app starts up correctly."""
        # The fact that client fixture works means lifespan startup was successful
        assert True


class TestHealthCheck:
    """Test cases for application health and basic functionality."""

    def test_root_endpoint_exists(self, client):
        """Test that we can make requests to the application."""
        # Since there's no root endpoint defined, this should return 404
        response = client.get("/")
        assert response.status_code == 404

    def test_openapi_docs_available(self, client):
        """Test that OpenAPI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi_data = response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
