# Real Backend

This is a backend application built with FastAPI, designed to serve as the API for a comprehensive e-commerce or inventory management system. It features JWT-based authentication, and CRUD operations for products, categories, brands, providers, customers, and sales.

[Frontend Link](https://github.com/Frknk/real-frontend)

## Features

- **Modern Tech Stack**: Built with Python 3.13, FastAPI, and SQLModel.
- **Authentication**: Secure JWT-based authentication and authorization.
- **Modular Routes**: Well-structured API endpoints for different resources (products, users, etc.).
- **Database**: Uses SQLModel for ORM, compatible with PostgreSQL.
- **Asynchronous**: Leverages FastAPI's async capabilities for high performance.
- **Testing**: Comprehensive test suite using `pytest`.
- **Containerized**: Ready to be deployed with Docker.
- **CI/CD**: GitHub Actions workflows for Continuous Integration and Continuous Deployment.

## Project Structure

```
.
├── src/
│   ├── app.py              # FastAPI app creation and configuration
│   ├── config.py           # Environment variable configuration
│   ├── database.py         # Database connection and session management
│   └── routes/             # API route modules
│       ├── auth/
│       ├── products/
│       ├── categories/
│       └── ...
├── tests/                  # Pytest test suite
│   ├── conftest.py         # Test fixtures
│   └── test_*.py           # Test files for different modules
├── main.py                 # Application entry point
├── pyproject.toml          # Project metadata and dependencies
├── Dockerfile              # Docker configuration for deployment
└── .github/workflows/      # CI/CD pipelines
```

## Getting Started

### Prerequisites

- Python 3.13+
- `uv` package manager
- A running PostgreSQL instance

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/real-backend.git
    cd real-backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```sh
    uv venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    uv sync
    ```

3.  **Set up environment variables:**
    Create a `.env` file by copying the example and fill in the required values.
    ```sh
    cp .env.example .env
    ```
    Your `.env` file should look like this:
    ```env
    SECRET_KEY="your_super_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES="30"
    ALLOWED_ORIGIN="http://localhost:3000" # Or your frontend URL
    DB_URL="postgresql+psycopg://user:password@host:port/dbname"
    ```

### Running the Application

To run the development server with live reloading:

```sh
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Documentation

Once the application is running, you can access the interactive API documentation at:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

## Testing

The project has a comprehensive test suite using `pytest`. The tests use an in-memory SQLite database to ensure isolation.

To run all tests:

```sh
pytest
```

To run tests with coverage:

```sh
pytest --cov=src
```

For more details on running specific tests, see the [Testing Guide](tests/README.md).

## Deployment

This project is configured for Docker-based deployment.

### Building the Docker Image

To build the Docker image:

```sh
docker build -t real-backend .
```

### Running with Docker

To run the application inside a Docker container:

```sh
docker run -d -p 8000:8000 --env-file .env --name real-backend-container real-backend
```

## Continuous Integration & Deployment (CI/CD)

This repository is equipped with GitHub Actions for:

-   **Continuous Integration (`ci.yml`)**: Automatically runs linters and the test suite on every push to the `master` branch.
-   **Continuous Deployment (`cd.yml`)**: Builds and pushes a Docker image to Docker Hub whenever a new release is created on GitHub.