"""Tests for Password Reset Flow."""
from datetime import datetime, timedelta


class TestForgotPassword:
    """Forgot password endpoint tests."""

    def test_forgot_password_existing_user(self, client):
        """Should accept request for existing user."""
        client.post("/api/v1/auth/register", json={
            "email": "forgot@simupharma.com",
            "name": "Forgot User",
            "password": "StrongPass123!",
        })

        response = client.post("/api/v1/auth/forgot-password", json={
            "email": "forgot@simupharma.com"
        })
        assert response.status_code == 200
        assert "reset link" in response.json()["message"].lower()

    def test_forgot_password_nonexistent_user(self, client):
        """Should return success even for non-existent users (prevent enumeration)."""
        response = client.post("/api/v1/auth/forgot-password", json={
            "email": "nobody@simupharma.com"
        })
        assert response.status_code == 200

    def test_forgot_password_generates_token(self, client):
        """Should generate a reset token in the database."""
        client.post("/api/v1/auth/register", json={
            "email": "token@simupharma.com",
            "name": "Token User",
            "password": "StrongPass123!",
        })

        client.post("/api/v1/auth/forgot-password", json={
            "email": "token@simupharma.com"
        })

        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "token@simupharma.com").first()
        assert user.password_reset_token is not None
        assert user.password_reset_token_expires is not None
        db.close()


class TestResetPassword:
    """Reset password endpoint tests."""

    def test_reset_password_valid_token(self, client):
        """Should reset password with valid token."""
        # Register
        client.post("/api/v1/auth/register", json={
            "email": "reset@simupharma.com",
            "name": "Reset User",
            "password": "OldPass123!",
        })

        # Request reset
        client.post("/api/v1/auth/forgot-password", json={
            "email": "reset@simupharma.com"
        })

        # Get token from DB
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "reset@simupharma.com").first()
        token = user.password_reset_token
        db.close()

        # Reset password
        response = client.post("/api/v1/auth/reset-password", json={
            "token": token,
            "new_password": "NewPass456!"
        })
        assert response.status_code == 200
        assert "reset successfully" in response.json()["message"].lower()

        # Login with new password should succeed
        login_response = client.post("/api/v1/auth/login", json={
            "email": "reset@simupharma.com",
            "password": "NewPass456!",
        })
        assert login_response.status_code == 200

        # Login with old password should fail
        old_login = client.post("/api/v1/auth/login", json={
            "email": "reset@simupharma.com",
            "password": "OldPass123!",
        })
        assert old_login.status_code == 401

    def test_reset_password_invalid_token(self, client):
        """Should reject invalid reset token."""
        response = client.post("/api/v1/auth/reset-password", json={
            "token": "invalid-token-xyz",
            "new_password": "NewPass456!"
        })
        assert response.status_code == 400

    def test_reset_password_expired_token(self, client):
        """Should reject expired reset token."""
        # Register and request reset
        client.post("/api/v1/auth/register", json={
            "email": "expiredreset@simupharma.com",
            "name": "Expired Reset",
            "password": "OldPass123!",
        })
        client.post("/api/v1/auth/forgot-password", json={
            "email": "expiredreset@simupharma.com"
        })

        # Expire the token
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "expiredreset@simupharma.com").first()
        token = user.password_reset_token
        user.password_reset_token_expires = datetime.utcnow() - timedelta(hours=1)
        db.commit()
        db.close()

        response = client.post("/api/v1/auth/reset-password", json={
            "token": token,
            "new_password": "NewPass456!"
        })
        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower()

    def test_reset_password_weak_password(self, client):
        """Should reject weak new passwords."""
        # Register and request reset
        client.post("/api/v1/auth/register", json={
            "email": "weakreset@simupharma.com",
            "name": "Weak Reset",
            "password": "OldPass123!",
        })
        client.post("/api/v1/auth/forgot-password", json={
            "email": "weakreset@simupharma.com"
        })

        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "weakreset@simupharma.com").first()
        token = user.password_reset_token
        db.close()

        response = client.post("/api/v1/auth/reset-password", json={
            "token": token,
            "new_password": "weak"
        })
        assert response.status_code == 400

    def test_reset_password_also_verifies_email(self, client):
        """Password reset should also verify the user's email."""
        # Register (unverified)
        client.post("/api/v1/auth/register", json={
            "email": "verifyreset@simupharma.com",
            "name": "Verify Reset",
            "password": "OldPass123!",
        })

        # Request reset
        client.post("/api/v1/auth/forgot-password", json={
            "email": "verifyreset@simupharma.com"
        })

        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "verifyreset@simupharma.com").first()
        token = user.password_reset_token
        assert user.is_verified is False
        db.close()

        # Reset password
        client.post("/api/v1/auth/reset-password", json={
            "token": token,
            "new_password": "NewPass456!"
        })

        # Check user is now verified
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "verifyreset@simupharma.com").first()
        assert user.is_verified is True
        db.close()
