"""Tests for Authentication — Register, Login, Profile (API v1)."""


class TestRegister:
    """Registration endpoint tests."""

    def test_register_success(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "new@simupharma.com",
            "name": "New User",
            "password": "StrongPass123!",
            "institution": "Test Uni"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "new@simupharma.com"
        assert data["user"]["name"] == "New User"
        assert data["user"]["role"] == "student"
        assert data["user"]["is_verified"] is False

    def test_register_duplicate_email(self, client):
        """Should reject duplicate emails."""
        payload = {
            "email": "dup@simupharma.com",
            "name": "User One",
            "password": "StrongPass123!",
        }
        client.post("/api/v1/auth/register", json=payload)
        response = client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_weak_password(self, client):
        """Should reject passwords shorter than 8 characters."""
        response = client.post("/api/v1/auth/register", json={
            "email": "weak@simupharma.com",
            "name": "Weak Pass User",
            "password": "short",
        })
        assert response.status_code == 400
        assert "8 characters" in response.json()["detail"]

    def test_register_password_no_uppercase(self, client):
        """Should reject passwords without uppercase letters."""
        response = client.post("/api/v1/auth/register", json={
            "email": "weak2@simupharma.com",
            "name": "Weak Pass User",
            "password": "nouppercase123!",
        })
        assert response.status_code == 400
        assert "uppercase" in response.json()["detail"]

    def test_register_password_no_special_char(self, client):
        """Should reject passwords without special characters."""
        response = client.post("/api/v1/auth/register", json={
            "email": "weak3@simupharma.com",
            "name": "Weak Pass User",
            "password": "NoSpecial123",
        })
        assert response.status_code == 400
        assert "special character" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Should reject invalid email formats."""
        response = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "name": "Bad Email User",
            "password": "StrongPass123!",
        })
        assert response.status_code == 422  # Pydantic validation error


class TestLogin:
    """Login endpoint tests."""

    def test_login_success(self, registered_user):
        client, user_data, _ = registered_user
        response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == user_data["email"]

    def test_login_wrong_password(self, registered_user):
        client, user_data, _ = registered_user
        response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": "WrongPassword1!",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/api/v1/auth/login", json={
            "email": "nobody@simupharma.com",
            "password": "SomePassword123!",
        })
        assert response.status_code == 401


class TestProfile:
    """Profile endpoint tests."""

    def test_get_me_authenticated(self, client):
        # Register a user first
        reg_response = client.post("/api/v1/auth/register", json={
            "email": "me@simupharma.com",
            "name": "Profile User",
            "password": "SecurePass123!",
            "institution": "Test Uni"
        })
        assert reg_response.status_code == 200
        token = reg_response.json()["access_token"]

        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@simupharma.com"
        assert data["name"] == "Profile User"
        assert "is_verified" in data

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_get_me_invalid_token(self, client):
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token-xyz"}
        )
        assert response.status_code == 401
