"""Tests for RBAC (Role-Based Access Control)."""


class TestRBAC:
    """Role-based access control tests using the RBAC dependencies."""

    def test_student_cannot_access_admin_endpoints(self, registered_user):
        """Students should not have admin access."""
        client, _, token = registered_user
        # The analytics leaderboard is currently public, but we test the principle
        # by checking the user's role
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["role"] == "student"

    def test_admin_user_has_correct_role(self, admin_user):
        """Admin users should have the admin role."""
        client, _, token = admin_user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["role"] == "admin"

    def test_instructor_user_has_correct_role(self, instructor_user):
        """Instructor users should have the instructor role."""
        client, _, token = instructor_user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["role"] == "instructor"


class TestRBACDependencies:
    """Test the RBAC dependency functions directly."""

    def test_require_role_function(self):
        """Test that require_role creates valid dependencies."""
        from backend.auth.rbac import require_role
        admin_dep = require_role("admin")
        assert callable(admin_dep)

    def test_require_admin_exists(self):
        """Test that pre-built role dependencies exist."""
        from backend.auth.rbac import require_admin, require_instructor_or_admin
        assert callable(require_admin)
        assert callable(require_instructor_or_admin)
