from fastapi import status


class TestSaleEndpoints:
    """Test cases for sale API endpoints."""

    def _create_prerequisites(self, client):
        """Create brand, category, provider, product, and customer for sale tests."""
        client.post("/brands", json={"name": "Sale Brand"})
        client.post(
            "/categories", json={"name": "Sale Category", "description": "desc"}
        )
        client.post(
            "/providers",
            json={
                "ruc": 987654321,
                "name": "Sale Provider",
                "address": "123 St",
                "phone": "555-0000",
                "email": "sale@provider.com",
            },
        )
        product_resp = client.post(
            "/products",
            json={
                "name": "Sale Product",
                "description": "A product for sale tests",
                "stock": 50,
                "price": 25.0,
                "provider_name": "Sale Provider",
                "category_name": "Sale Category",
                "brand_name": "Sale Brand",
            },
        )
        customer_resp = client.post(
            "/customers",
            json={
                "dni": 11223344,
                "name": "Sale",
                "last_name": "Customer",
                "email": "sale@customer.com",
            },
        )
        product = product_resp.json()
        customer = customer_resp.json()
        return product, customer

    def test_create_sale_success(self, client):
        """Test successful sale creation."""
        product, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [{"product_id": product["id"], "quantity": 2}],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_200_OK
        sale = response.json()
        assert sale["total"] == 50.0
        assert sale["customer_dni"] == customer["dni"]

    def test_create_sale_missing_customer(self, client):
        """Test sale creation with non-existent customer."""
        product, _ = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": 99999999,
            "products": [{"product_id": product["id"], "quantity": 1}],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in response.json()["detail"]

    def test_create_sale_missing_product(self, client):
        """Test sale creation with non-existent product."""
        _, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [{"product_id": 99999, "quantity": 1}],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_create_sale_insufficient_stock(self, client):
        """Test sale creation with insufficient stock."""
        product, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [{"product_id": product["id"], "quantity": 9999}],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Not enough stock" in response.json()["detail"]

    def test_create_sale_empty_products(self, client):
        """Test sale creation with empty products list."""
        _, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No products provided" in response.json()["detail"]

    def test_create_sale_zero_quantity(self, client):
        """Test sale creation with zero quantity (rejected by schema gt=0)."""
        product, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [{"product_id": product["id"], "quantity": 0}],
        }
        response = client.post("/sales/", json=sale_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_read_sale_success(self, client):
        """Test reading a sale by ID."""
        product, customer = self._create_prerequisites(client)

        sale_data = {
            "customer_dni": customer["dni"],
            "products": [{"product_id": product["id"], "quantity": 3}],
        }
        create_resp = client.post("/sales/", json=sale_data)
        sale_id = create_resp.json()["id"]

        response = client.get(f"/sales/{sale_id}")

        assert response.status_code == status.HTTP_200_OK
        sale = response.json()
        assert sale["id"] == sale_id
        assert sale["total"] == 75.0
        assert len(sale["products"]) == 1
        assert sale["products"][0]["name"] == "Sale Product"
        assert sale["customer"]["dni"] == customer["dni"]

    def test_read_sale_not_found(self, client):
        """Test reading a non-existent sale."""
        response = client.get("/sales/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_read_all_sales(self, client):
        """Test reading all sales."""
        response = client.get("/sales/")

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
