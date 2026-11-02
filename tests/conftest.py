"""Test Configuration — Shared fixtures for SimuPharma tests.

Uses an in-memory SQLite database so tests are fast and isolated.
Disables rate limiting to avoid 429 errors during test execution.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set environment to development before importing app
os.environ["ENVIRONMENT"] = "development"

from backend.database import Base, get_db
from backend.main import app, limiter
from backend.auth.router import auth_limiter


# ---- Disable rate limiting in tests ----
limiter.enabled = False
auth_limiter.enabled = False


# ---- In-memory test database ----
TEST_DATABASE_URL = "sqlite:///./test_simupharma.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the database dependency for all tests
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    """Register a test user and return (client, user_data, token)."""
    user_data = {
        "email": "test@simupharma.com",
        "name": "Test Student",
        "password": "SecurePass123!",
        "institution": "Test University"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    token = response.json()["access_token"]
    return client, user_data, token


@pytest.fixture
def auth_headers(registered_user):
    """Return Authorization headers for authenticated requests."""
    _, _, token = registered_user
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_user(client):
    """Register a user and promote to admin, return (client, user_data, token, db)."""
    user_data = {
        "email": "admin@simupharma.com",
        "name": "Admin User",
        "password": "AdminPass123!",
        "institution": "SimuPharma HQ"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Promote to admin directly in DB
    db = TestSessionLocal()
    from backend.models import User
    user = db.query(User).filter(User.email == "admin@simupharma.com").first()
    user.role = "admin"
    user.is_verified = True
    db.commit()
    db.close()

    return client, user_data, token


@pytest.fixture
def instructor_user(client):
    """Register a user and promote to instructor."""
    user_data = {
        "email": "instructor@simupharma.com",
        "name": "Instructor User",
        "password": "InstructorPass123!",
        "institution": "Test University"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Promote to instructor
    db = TestSessionLocal()
    from backend.models import User
    user = db.query(User).filter(User.email == "instructor@simupharma.com").first()
    user.role = "instructor"
    user.is_verified = True
    db.commit()
    db.close()

    return client, user_data, token
