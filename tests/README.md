# Testing Guide

This document provides information about the test suite 

## Test Structure

```
tests/
├── conftest.py                 # Test fixtures and configuration
├── test_app.py                # Application-level tests
├── test_database.py           # Database functionality tests
├── test_auth_operations.py    # Authentication operations tests
├── test_auth_endpoints.py     # Authentication API endpoint tests
├── test_products.py           # Product API tests
└── test_categories.py         # Category API tests
```

## Test Categories

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Unit tests (isolated functionality)
- `@pytest.mark.integration` - Integration tests (multiple components)
- `@pytest.mark.auth` - Authentication-related tests
- `@pytest.mark.database` - Database-dependent tests
- `@pytest.mark.slow` - Slow-running tests

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_auth_endpoints.py

# Run specific test method
python -m pytest tests/test_auth_endpoints.py::TestAuthEndpoints::test_login_success
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run only auth tests
python run_tests.py --auth

# Run specific test file with verbose output
python run_tests.py tests/test_products.py -v
```

### Test Filtering

```bash
# Run tests by marker
python -m pytest -m "unit"
python -m pytest -m "not slow"
python -m pytest -m "auth and not integration"

# Run tests matching pattern
python -m pytest -k "test_login"
python -m pytest -k "auth or product"
```

## Test Configuration

### Environment Setup

Tests use a separate SQLite database for isolation. Environment variables are mocked for testing:

- `SECRET_KEY`: Test secret key
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `ALLOWED_ORIGIN`: http://localhost:3000
- `DB_URL`: Test database URL

### Fixtures

Common fixtures available in all tests:

- `client`: FastAPI test client
- `test_db`: Test database engine
- `test_session`: Database session for tests
- `sample_user_data`: Sample user data for auth tests
- `sample_product_data`: Sample product data
- `sample_category_data`: Sample category data
- `authenticated_headers`: Authentication headers for protected endpoints

## Writing New Tests

### Test File Structure

```python
import pytest
from fastapi import status


class TestYourFeature:
    """Test cases for your feature."""
    
    def test_specific_functionality(self, client, sample_data):
        """Test description."""
        # Arrange
        # Act
        response = client.get("/your-endpoint")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_data


@pytest.mark.integration
class TestYourFeatureIntegration:
    """Integration tests for your feature."""
    
    def test_full_workflow(self, client):
        """Test complete workflow."""
        # Test multiple operations together
        pass
```

### Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Follow AAA pattern** (Arrange, Act, Assert)
3. **Use appropriate markers** to categorize tests
4. **Mock external dependencies** to keep tests isolated
5. **Test both success and failure cases**
6. **Use fixtures** for common test data
7. **Keep tests independent** - they should not depend on each other

### Testing API Endpoints

```python
def test_create_item_success(self, client, sample_item_data):
    """Test successful item creation."""
    response = client.post("/items", json=sample_item_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    created_item = response.json()
    assert created_item["name"] == sample_item_data["name"]
    assert "id" in created_item

def test_create_item_invalid_data(self, client):
    """Test item creation with invalid data."""
    invalid_data = {"name": ""}  # Invalid according to your validation rules
    
    response = client.post("/items", json=invalid_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
```

### Testing Authentication

For endpoints that require authentication:

```python
def test_protected_endpoint(self, client, authenticated_headers):
    """Test accessing protected endpoint."""
    response = client.get("/protected", headers=authenticated_headers)
    
    assert response.status_code == status.HTTP_200_OK

def test_protected_endpoint_unauthorized(self, client):
    """Test accessing protected endpoint without auth."""
    response = client.get("/protected")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

## Coverage Reports

When running with coverage, reports are generated in:
- `htmlcov/index.html` - HTML coverage report
- Terminal output shows coverage percentage

## Continuous Integration

Add to your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    python -m pytest --cov=src --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v1
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Common Issues

1. **Database errors**: Ensure test database is properly isolated
2. **Import errors**: Check that `src` is in Python path
3. **Fixture not found**: Make sure `conftest.py` is in the right location
4. **Authentication failures**: Verify mock environment variables

### Debug Mode

Run tests with debugging:

```bash
# Drop into debugger on failure
python -m pytest --pdb

# Show local variables in traceback
python -m pytest -l

# Stop on first failure
python -m pytest -x
```
