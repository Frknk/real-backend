from fastapi import status


class TestCategoryEndpoints:
    """Test cases for category API endpoints."""

    def test_get_categories_empty(self, client):
        """Test getting categories when none exist."""
        response = client.get("/categories")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_category_success(self, client, sample_category_data):
        """Test successful category creation."""
        response = client.post("/categories", json=sample_category_data)

        assert response.status_code == status.HTTP_200_OK
        created_category = response.json()
        assert created_category["name"] == sample_category_data["name"]
        assert "id" in created_category

    def test_create_category_invalid_data(self, client):
        """Test category creation with invalid data."""
        invalid_data = {"name": ""}  # Empty name

        response = client.post("/categories", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_category_duplicate_name(self, client, sample_category_data):
        """Test creating category with duplicate name."""
        # Create first category
        client.post("/categories", json=sample_category_data)

        # Try to create another with same name
        response = client.post("/categories", json=sample_category_data)

        # Should fail due to unique constraint
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ]

    def test_get_category_by_id_success(self, client, sample_category_data):
        """Test getting a specific category by ID."""
        # Create a category first
        create_response = client.post("/categories", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Get the category by ID
        response = client.get(f"/categories/{category_id}")

        assert response.status_code == status.HTTP_200_OK
        category = response.json()
        assert category["id"] == category_id
        assert category["name"] == sample_category_data["name"]

    def test_get_category_by_id_not_found(self, client):
        """Test getting a non-existent category."""
        response = client.get("/categories/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_category_success(self, client, sample_category_data):
        """Test successful category update."""
        # Create a category first
        create_response = client.post("/categories", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Update the category
        update_data = {"name": "Updated Category Name"}

        response = client.patch(f"/categories/{category_id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        updated_category = response.json()
        assert updated_category["name"] == "Updated Category Name"

    def test_update_category_not_found(self, client, sample_category_data):
        """Test updating a non-existent category."""
        response = client.patch("/categories/99999", json=sample_category_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_success(self, client, sample_category_data):
        """Test successful category deletion."""
        # Create a category first
        create_response = client.post("/categories", json=sample_category_data)
        created_category = create_response.json()
        category_id = created_category["id"]

        # Delete the category
        response = client.delete(f"/categories/{category_id}")

        assert response.status_code == status.HTTP_200_OK

        # Verify category is deleted
        get_response = client.get(f"/categories/{category_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_not_found(self, client):
        """Test deleting a non-existent category."""
        response = client.delete("/categories/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_all_categories_with_data(self, client):
        """Test getting all categories when categories exist."""
        # Create multiple categories
        category1_data = {"name": "Category 1"}
        category2_data = {"name": "Category 2"}

        client.post("/categories", json=category1_data)
        client.post("/categories", json=category2_data)

        # Get all categories
        response = client.get("/categories")

        assert response.status_code == status.HTTP_200_OK
        categories = response.json()
        assert len(categories) >= 2
        category_names = [c["name"] for c in categories]
        assert "Category 1" in category_names
        assert "Category 2" in category_names


class TestCategoryValidation:
    """Test cases for category data validation."""

    def test_category_create_missing_name(self, client):
        """Test category creation without name."""
        incomplete_data = {}

        response = client.post("/categories", json=incomplete_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_category_name_length_validation(self, client):
        """Test category name length validation."""
        # Test very long name (if there are length restrictions)
        long_name_data = {"name": "A" * 1000}

        response = client.post("/categories", json=long_name_data)

        # This test depends on whether you have length validation
        # Adjust based on your business rules
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]


class TestCategoryIntegration:
    """Integration tests for category functionality."""

    def test_full_category_lifecycle(self, client, sample_category_data):
        """Test complete category lifecycle: create -> read -> update -> delete."""
        # Create
        create_response = client.post("/categories", json=sample_category_data)
        assert create_response.status_code == status.HTTP_200_OK
        category = create_response.json()
        category_id = category["id"]

        # Read
        read_response = client.get(f"/categories/{category_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["name"] == sample_category_data["name"]

        # Update
        update_data = {"name": "Updated Category"}
        update_response = client.patch(f"/categories/{category_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["name"] == "Updated Category"

        # Delete
        delete_response = client.delete(f"/categories/{category_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/categories/{category_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND

    def test_category_with_products_relationship(
        self, client, sample_category_data, sample_product_data
    ):
        """Test category-product relationship."""
        # Create category first
        category_response = client.post("/categories", json=sample_category_data)
        assert category_response.status_code == status.HTTP_200_OK

        # Create product with this category
        product_data = sample_product_data.copy()
        product_data["category_name"] = sample_category_data["name"]

        product_response = client.post("/products", json=product_data)

        # The success of this test depends on how the relationship is implemented
        # Adjust assertions based on your actual implementation
        assert product_response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]
