"""Tests for Email Verification Flow."""
from datetime import datetime, timedelta


class TestEmailVerification:
    """Email verification endpoint tests."""

    def test_register_creates_unverified_user(self, client):
        """Registration should create a user with is_verified=False."""
        response = client.post("/api/v1/auth/register", json={
            "email": "verify@simupharma.com",
            "name": "Verify User",
            "password": "StrongPass123!",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["is_verified"] is False

    def test_verify_email_valid_token(self, client):
        """Should verify email with a valid token."""
        # Register
        client.post("/api/v1/auth/register", json={
            "email": "vtoken@simupharma.com",
            "name": "Token User",
            "password": "StrongPass123!",
        })

        # Get token from DB
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "vtoken@simupharma.com").first()
        token = user.verification_token
        db.close()

        assert token is not None

        # Verify email
        response = client.post("/api/v1/auth/verify-email", json={"token": token})
        assert response.status_code == 200
        assert "verified" in response.json()["message"].lower()

        # Check user is now verified
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "vtoken@simupharma.com").first()
        assert user.is_verified is True
        assert user.verification_token is None
        db.close()

    def test_verify_email_invalid_token(self, client):
        """Should reject invalid verification token."""
        response = client.post("/api/v1/auth/verify-email", json={"token": "invalid-token-xyz"})
        assert response.status_code == 400

    def test_verify_email_expired_token(self, client):
        """Should reject expired verification token."""
        # Register
        client.post("/api/v1/auth/register", json={
            "email": "expired@simupharma.com",
            "name": "Expired User",
            "password": "StrongPass123!",
        })

        # Expire the token
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "expired@simupharma.com").first()
        token = user.verification_token
        user.verification_token_expires = datetime.utcnow() - timedelta(hours=1)
        db.commit()
        db.close()

        # Try to verify
        response = client.post("/api/v1/auth/verify-email", json={"token": token})
        assert response.status_code == 400
        assert "expired" in response.json()["detail"].lower()

    def test_verify_email_already_verified(self, client):
        """Should return success message if already verified."""
        # Register and verify
        client.post("/api/v1/auth/register", json={
            "email": "already@simupharma.com",
            "name": "Already Verified",
            "password": "StrongPass123!",
        })
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "already@simupharma.com").first()
        token = user.verification_token
        user.is_verified = True
        db.commit()
        db.close()

        response = client.post("/api/v1/auth/verify-email", json={"token": token})
        assert response.status_code == 200
        assert "already" in response.json()["message"].lower()


class TestResendVerification:
    """Resend verification endpoint tests."""

    def test_resend_verification(self, client):
        """Should allow resending verification email."""
        client.post("/api/v1/auth/register", json={
            "email": "resend@simupharma.com",
            "name": "Resend User",
            "password": "StrongPass123!",
        })

        response = client.post("/api/v1/auth/resend-verification", json={
            "email": "resend@simupharma.com"
        })
        assert response.status_code == 200

    def test_resend_verification_nonexistent_email(self, client):
        """Should return success even for non-existent emails (prevent enumeration)."""
        response = client.post("/api/v1/auth/resend-verification", json={
            "email": "nobody@simupharma.com"
        })
        assert response.status_code == 200

    def test_resend_verification_already_verified(self, client):
        """Should return success for already verified users (prevent enumeration)."""
        client.post("/api/v1/auth/register", json={
            "email": "alreadyv@simupharma.com",
            "name": "Already User",
            "password": "StrongPass123!",
        })

        # Verify the user
        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "alreadyv@simupharma.com").first()
        user.is_verified = True
        db.commit()
        db.close()

        response = client.post("/api/v1/auth/resend-verification", json={
            "email": "alreadyv@simupharma.com"
        })
        assert response.status_code == 200
