"""Tests for Security Hardening — Headers, Password Validation, Request IDs."""


class TestSecurityHeaders:
    """Security header tests."""

    def test_security_headers_present(self, client):
        """All responses should include security headers."""
        response = client.get("/api/health")
        assert response.status_code == 200

        # Check security headers
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
        assert "camera=()" in response.headers.get("Permissions-Policy", "")

    def test_request_id_present(self, client):
        """All responses should include a unique X-Request-ID."""
        response1 = client.get("/api/health")
        response2 = client.get("/api/health")

        rid1 = response1.headers.get("X-Request-ID")
        rid2 = response2.headers.get("X-Request-ID")

        assert rid1 is not None
        assert rid2 is not None
        assert rid1 != rid2  # Each request gets a unique ID

    def test_security_headers_on_api_endpoints(self, client):
        """Security headers should be on API endpoints too."""
        response = client.post("/api/v1/simulate/uvvis", json={
            "peaks": [{"center": 254, "epsilon": 10000, "width": 20}],
            "concentration": 0.001,
        })
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Request-ID") is not None


class TestPasswordValidation:
    """Password strength validation tests."""

    def test_password_requires_min_length(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw1@test.com", "name": "Test", "password": "Ab1!"
        })
        assert response.status_code == 400
        assert "8 characters" in response.json()["detail"]

    def test_password_requires_uppercase(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw2@test.com", "name": "Test", "password": "lowercase123!"
        })
        assert response.status_code == 400
        assert "uppercase" in response.json()["detail"]

    def test_password_requires_lowercase(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw3@test.com", "name": "Test", "password": "UPPERCASE123!"
        })
        assert response.status_code == 400
        assert "lowercase" in response.json()["detail"]

    def test_password_requires_digit(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw4@test.com", "name": "Test", "password": "NoDigits!abc"
        })
        assert response.status_code == 400
        assert "digit" in response.json()["detail"]

    def test_password_requires_special_char(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw5@test.com", "name": "Test", "password": "NoSpecial123"
        })
        assert response.status_code == 400
        assert "special character" in response.json()["detail"]

    def test_strong_password_passes(self, client):
        response = client.post("/api/v1/auth/register", json={
            "email": "pw6@test.com", "name": "Test", "password": "StrongPass123!"
        })
        assert response.status_code == 200


class TestAPIVersioning:
    """API versioning tests."""

    def test_v1_health_check(self, client):
        """Health check should be at /api/health (unversioned)."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_v1_auth_register(self, client):
        """Auth register should be at /api/v1/auth/register."""
        response = client.post("/api/v1/auth/register", json={
            "email": "v1test@simupharma.com",
            "name": "V1 Test",
            "password": "StrongPass123!",
        })
        assert response.status_code == 200

    def test_v1_simulate_endpoint(self, client):
        """Simulation endpoints should be at /api/v1/simulate/."""
        response = client.post("/api/v1/simulate/polarimeter", json={
            "specific_rotation": 52.7,
            "concentration": 0.1,
        })
        assert response.status_code == 200
