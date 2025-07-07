import pytest
from fastapi import status


class TestBrandEndpoints:
    """Test cases for brand API endpoints."""

    def test_get_brands_empty(self, client):
        """Test getting brands when none exist."""
        response = client.get("/brands")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_brand_success(self, client, sample_brand_data):
        """Test successful brand creation."""
        response = client.post("/brands", json=sample_brand_data)

        assert response.status_code == status.HTTP_200_OK
        created_brand = response.json()
        assert created_brand["name"] == sample_brand_data["name"]
        assert "id" in created_brand

    def test_create_brand_invalid_data(self, client):
        """Test brand creation with invalid data."""
        invalid_data = {"name": ""}  # Empty name

        response = client.post("/brands", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_brand_by_id_success(self, client, sample_brand_data):
        """Test getting a specific brand by ID."""
        # Create a brand first
        create_response = client.post("/brands", json=sample_brand_data)
        created_brand = create_response.json()
        brand_id = created_brand["id"]

        # Get the brand by ID
        response = client.get(f"/brands/{brand_id}")

        assert response.status_code == status.HTTP_200_OK
        brand = response.json()
        assert brand["id"] == brand_id
        assert brand["name"] == sample_brand_data["name"]

    def test_get_brand_by_id_not_found(self, client):
        """Test getting a non-existent brand."""
        response = client.get("/brands/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_brand_success(self, client, sample_brand_data):
        """Test successful brand update."""
        # Create a brand first
        create_response = client.post("/brands", json=sample_brand_data)
        created_brand = create_response.json()
        brand_id = created_brand["id"]

        # Update the brand
        update_data = sample_brand_data.copy()
        update_data["name"] = "Updated Brand Name"

        response = client.patch(f"/brands/{brand_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        updated_brand = response.json()
        assert updated_brand["name"] == "Updated Brand Name"

    def test_delete_brand_success(self, client, sample_brand_data):
        """Test successful brand deletion."""
        # Create a brand first
        create_response = client.post("/brands", json=sample_brand_data)
        created_brand = create_response.json()
        brand_id = created_brand["id"]

        # Delete the brand
        response = client.delete(f"/brands/{brand_id}")

        assert response.status_code == status.HTTP_200_OK

        # Verify brand is deleted
        get_response = client.get(f"/brands/{brand_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestProviderEndpoints:
    """Test cases for provider API endpoints."""

    def test_get_providers_empty(self, client):
        """Test getting providers when none exist."""
        response = client.get("/providers")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_provider_success(self, client, sample_provider_data):
        """Test successful provider creation."""
        response = client.post("/providers", json=sample_provider_data)

        assert response.status_code == status.HTTP_200_OK
        created_provider = response.json()
        assert created_provider["name"] == sample_provider_data["name"]
        assert "id" in created_provider

    def test_get_provider_by_id_success(self, client, sample_provider_data):
        """Test getting a specific provider by ID."""
        # Create a provider first
        create_response = client.post("/providers", json=sample_provider_data)
        created_provider = create_response.json()
        provider_id = created_provider["id"]

        # Get the provider by ID
        response = client.get(f"/providers/{provider_id}")

        assert response.status_code == status.HTTP_200_OK
        provider = response.json()
        assert provider["id"] == provider_id
        assert provider["name"] == sample_provider_data["name"]

    def test_update_provider_success(self, client, sample_provider_data):
        """Test successful provider update."""
        # Create a provider first
        create_response = client.post("/providers", json=sample_provider_data)
        created_provider = create_response.json()
        provider_id = created_provider["id"]

        # Update the provider
        update_data = sample_provider_data.copy()
        update_data["name"] = "Updated Provider Name"

        response = client.patch(f"/providers/{provider_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        updated_provider = response.json()
        assert updated_provider["name"] == "Updated Provider Name"

    def test_delete_provider_success(self, client, sample_provider_data):
        """Test successful provider deletion."""
        # Create a provider first
        create_response = client.post("/providers", json=sample_provider_data)
        created_provider = create_response.json()
        provider_id = created_provider["id"]

        # Delete the provider
        response = client.delete(f"/providers/{provider_id}")

        assert response.status_code == status.HTTP_200_OK

        # Verify provider is deleted
        get_response = client.get(f"/providers/{provider_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestCustomerEndpoints:
    """Test cases for customer API endpoints."""

    def test_get_customers_empty(self, client):
        """Test getting customers when none exist."""
        response = client.get("/customers")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_customer_success(self, client, sample_customer_data):
        """Test successful customer creation."""
        response = client.post("/customers", json=sample_customer_data)
        print(response.json())  # Debugging line to see the response
        assert response.status_code == status.HTTP_200_OK
        created_customer = response.json()
        assert created_customer["name"] == sample_customer_data["name"]
        assert created_customer["email"] == sample_customer_data["email"]
        assert "id" in created_customer

    def test_get_customer_by_dni_success(self, client, sample_customer_data):
        """Test getting a specific customer by ID."""
        # Create a customer first
        create_response = client.post("/customers", json=sample_customer_data)
        created_customer = create_response.json()
        customer_id = created_customer["dni"]

        # Get the customer by ID
        response = client.get(f"/customers/{customer_id}")

        assert response.status_code == status.HTTP_200_OK
        customer = response.json()
        assert customer["dni"] == customer_id
        assert customer["name"] == sample_customer_data["name"]

    # def test_update_customer_success(self, client, sample_customer_data):
    #     """Test successful customer update."""
    #     # Create a customer first
    #     create_response = client.post("/customers", json=sample_customer_data)
    #     created_customer = create_response.json()
    #     customer_id = created_customer["id"]
    #
    #     # Update the customer
    #     update_data = sample_customer_data.copy()
    #     update_data["name"] = "Updated Customer Name"
    #
    #     response = client.patch(f"/customers/{customer_id}", json=update_data)
    #
    #     assert response.status_code == status.HTTP_200_OK
    #     updated_customer = response.json()
    #     assert updated_customer["name"] == "Updated Customer Name"
    #
    # def test_delete_customer_success(self, client, sample_customer_data):
    #     """Test successful customer deletion."""
    #     # Create a customer first
    #     create_response = client.post("/customers", json=sample_customer_data)
    #     created_customer = create_response.json()
    #     customer_id = created_customer["id"]
    #
    #     # Delete the customer
    #     response = client.delete(f"/customers/{customer_id}")
    #
    #     assert response.status_code == status.HTTP_200_OK
    #
    #     # Verify customer is deleted
    #     get_response = client.get(f"/customers/{customer_id}")
    #     assert get_response.status_code == status.HTTP_404_NOT_FOUND
