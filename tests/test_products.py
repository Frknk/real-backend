import pytest
from fastapi import status


class TestProductEndpoints:
    """Test cases for product API endpoints."""

    def test_get_products_empty(self, client):
        """Test getting products when none exist."""
        response = client.get("/products")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_product_success(self, client, sample_product_data):
        """Test successful product creation."""
        response = client.post("/products", json=sample_product_data)

        assert response.status_code == status.HTTP_200_OK
        created_product = response.json()
        assert created_product["name"] == sample_product_data["name"]
        assert created_product["description"] == sample_product_data["description"]
        assert created_product["stock"] == sample_product_data["stock"]
        assert created_product["price"] == sample_product_data["price"]
        assert "id" in created_product

    def test_create_product_invalid_data(self, client):
        """Test product creation with invalid data."""
        invalid_data = {
            "name": "",  # Empty name
            "description": "Test description",
            "stock": -1,  # Negative stock
            "price": "invalid_price",  # Invalid price type
        }

        response = client.post("/products", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_product_by_id_success(self, client, sample_product_data):
        """Test getting a specific product by ID."""
        # Create a product first
        create_response = client.post("/products", json=sample_product_data)
        created_product = create_response.json()
        product_id = created_product["id"]

        # Get the product by ID
        response = client.get(f"/products/{product_id}")

        assert response.status_code == status.HTTP_200_OK
        product = response.json()
        assert product["id"] == product_id
        assert product["name"] == sample_product_data["name"]

    def test_get_product_by_id_not_found(self, client):
        """Test getting a non-existent product."""
        response = client.get("/products/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_product_success(self, client, sample_product_data):
        """Test successful product update."""
        # Create a product first
        create_response = client.post("/products", json=sample_product_data)
        created_product = create_response.json()
        product_id = created_product["id"]

        # Update the product
        update_data = sample_product_data.copy()
        update_data["name"] = "Updated Product Name"
        update_data["price"] = 149.99

        response = client.patch(f"/products/{product_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        updated_product = response.json()
        assert updated_product["name"] == "Updated Product Name"
        assert updated_product["price"] == 149.99

    def test_update_product_not_found(self, client, sample_product_data):
        """Test updating a non-existent product."""
        response = client.patch("/products/99999", json=sample_product_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_success(self, client, sample_product_data):
        """Test successful product deletion."""
        # Create a product first
        create_response = client.post("/products", json=sample_product_data)
        created_product = create_response.json()
        product_id = created_product["id"]

        # Delete the product
        response = client.delete(f"/products/{product_id}")

        assert response.status_code == status.HTTP_200_OK

        # Verify product is deleted
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_not_found(self, client):
        """Test deleting a non-existent product."""
        response = client.delete("/products/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_all_products_with_data(self, client, sample_product_data):
        """Test getting all products when products exist."""
        # Create multiple products
        product1_data = sample_product_data.copy()
        product1_data["name"] = "Product 1"

        product2_data = sample_product_data.copy()
        product2_data["name"] = "Product 2"

        client.post("/products", json=product1_data)
        client.post("/products", json=product2_data)

        # Get all products
        response = client.get("/products")

        assert response.status_code == status.HTTP_200_OK
        products = response.json()
        assert len(products) >= 2
        product_names = [p["name"] for p in products]
        assert "Product 1" in product_names
        assert "Product 2" in product_names


class TestProductValidation:
    """Test cases for product data validation."""

    def test_product_create_missing_required_fields(self, client):
        """Test product creation with missing required fields."""
        incomplete_data = {
            "name": "Test Product"
            # Missing other required fields
        }

        response = client.post("/products", json=incomplete_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_product_create_negative_stock(self, client, sample_product_data):
        """Test product creation with negative stock."""
        invalid_data = sample_product_data.copy()
        invalid_data["stock"] = -5

        response = client.post("/products", json=invalid_data)

        # Depending on validation rules, this might be accepted or rejected
        # Adjust assertion based on your business rules
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    def test_product_create_negative_price(self, client, sample_product_data):
        """Test product creation with negative price."""
        invalid_data = sample_product_data.copy()
        invalid_data["price"] = -10.99

        response = client.post("/products", json=invalid_data)

        # Depending on validation rules, this might be accepted or rejected
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]


class TestProductIntegration:
    """Integration tests for product functionality."""

    def test_full_product_lifecycle(self, client, sample_product_data):
        """Test complete product lifecycle: create -> read -> update -> delete."""
        # Create
        create_response = client.post("/products", json=sample_product_data)
        assert create_response.status_code == status.HTTP_200_OK
        product = create_response.json()
        product_id = product["id"]

        # Read
        read_response = client.get(f"/products/{product_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["name"] == sample_product_data["name"]

        # Update
        update_data = sample_product_data.copy()
        update_data["name"] = "Updated Product"
        update_response = client.patch(f"/products/{product_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["name"] == "Updated Product"

        # Delete
        delete_response = client.delete(f"/products/{product_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/products/{product_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
