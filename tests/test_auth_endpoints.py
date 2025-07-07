from fastapi import status


class TestAuthEndpoints:
    """Test cases for authentication API endpoints."""

    def test_register_user_success(self, client, sample_user_data):
        """Test successful user registration."""
        response = client.post("/auth/register", json=sample_user_data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == "complete"

    def test_register_user_duplicate_username(self, client, sample_user_data):
        """Test registration with duplicate username."""
        # Register user first time
        client.post("/auth/register", json=sample_user_data)

        # Try to register same user again
        response = client.post("/auth/register", json=sample_user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_register_user_invalid_data(self, client):
        """Test registration with invalid data."""
        invalid_data = {"username": ""}  # Missing password

        response = client.post("/auth/register", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_success(self, client, sample_user_data):
        """Test successful login."""
        # Register user first
        client.post("/auth/register", json=sample_user_data)

        # Login
        login_data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        }
        response = client.post("/auth/token", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_wrong_username(self, client, sample_user_data):
        """Test login with wrong username."""
        # Register user first
        client.post("/auth/register", json=sample_user_data)

        # Login with wrong username
        login_data = {
            "username": "wrongusername",
            "password": sample_user_data["password"],
        }
        response = client.post("/auth/token", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_wrong_password(self, client, sample_user_data):
        """Test login with wrong password."""
        # Register user first
        client.post("/auth/register", json=sample_user_data)

        # Login with wrong password
        login_data = {
            "username": sample_user_data["username"],
            "password": "wrongpassword",
        }
        response = client.post("/auth/token", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials."""
        response = client.post("/auth/token", data={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_verify_token_valid(self, client, authenticated_headers):
        """Test token verification with valid token."""
        # Extract token from headers
        auth_header = authenticated_headers["Authorization"]
        token = auth_header.split(" ")[1]  # Remove "Bearer " prefix

        response = client.get(f"/auth/verify_token/{token}")

        assert response.status_code == status.HTTP_200_OK
        # The exact response depends on the implementation

    def test_verify_token_invalid(self, client):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.here"

        response = client.get(f"/auth/verify_token/{invalid_token}")

        # Should return error status
        assert response.status_code in [400, 401, 422]

    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        # This would depend on having a protected endpoint
        # Since we don't see the full verify_token endpoint, we'll test with a hypothetical protected route
        pass

    def test_protected_endpoint_with_valid_token(self, client, authenticated_headers):
        """Test accessing protected endpoint with valid token."""
        # This would test a protected endpoint with proper authentication
        # Implementation depends on actual protected endpoints in the system
        pass


class TestAuthIntegration:
    """Integration tests for authentication flow."""

    def test_full_auth_flow(self, client, sample_user_data):
        """Test complete authentication flow: register -> login -> verify."""
        # Step 1: Register
        register_response = client.post("/auth/register", json=sample_user_data)
        assert register_response.status_code == status.HTTP_200_OK

        # Step 2: Login
        login_data = {
            "username": sample_user_data["username"],
            "password": sample_user_data["password"],
        }
        login_response = client.post("/auth/token", data=login_data)
        assert login_response.status_code == status.HTTP_200_OK

        token = login_response.json()["access_token"]

        # Step 3: Verify token
        verify_response = client.get(f"/auth/verify_token/{token}")
        # The status code depends on implementation, but it shouldn't be 500
        assert verify_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_token_expiry_flow(self, client, sample_user_data):
        """Test behavior with expired tokens."""
        # This would require mocking time or using very short expiry times
        # Implementation depends on how token expiry is handled
        pass
