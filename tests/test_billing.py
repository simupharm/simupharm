"""Tests for Billing — Plans, Subscription, Feature Gating (Razorpay)."""


class TestPlansEndpoint:
    """Plans endpoint tests."""

    def test_get_plans_returns_all_tiers(self, client):
        """Should return free, pro, and institution plans."""
        response = client.get("/api/v1/billing/plans")
        assert response.status_code == 200
        data = response.json()
        assert "plans" in data
        plan_ids = [p["id"] for p in data["plans"]]
        assert "free" in plan_ids
        assert "pro" in plan_ids
        assert "institution_starter" in plan_ids
        assert "institution_standard" in plan_ids
        assert "institution_premium" in plan_ids

    def test_free_plan_has_correct_instruments(self, client):
        """Free plan should include UV-Vis, Polarimeter, PSA only."""
        response = client.get("/api/v1/billing/plans")
        data = response.json()
        free_plan = next(p for p in data["plans"] if p["id"] == "free")
        assert set(free_plan["instruments"]) == {"uvvis", "polarimeter", "psa"}
        assert free_plan["daily_simulation_limit"] == 5

    def test_pro_plan_has_all_instruments(self, client):
        """Pro plan should include all 7 instruments."""
        response = client.get("/api/v1/billing/plans")
        data = response.json()
        pro_plan = next(p for p in data["plans"] if p["id"] == "pro")
        assert len(pro_plan["instruments"]) == 7
        assert pro_plan["daily_simulation_limit"] is None  # Unlimited

    def test_pro_plan_has_correct_pricing(self, client):
        """Pro plan should have monthly, semester, and annual prices in INR."""
        response = client.get("/api/v1/billing/plans")
        data = response.json()
        pro_plan = next(p for p in data["plans"] if p["id"] == "pro")
        assert "monthly" in pro_plan["prices"]
        assert "semester" in pro_plan["prices"]
        assert "annual" in pro_plan["prices"]
        assert pro_plan["prices"]["monthly"]["amount"] == 19900  # ₹199 in paise
        assert pro_plan["prices"]["semester"]["amount"] == 79900  # ₹799
        assert pro_plan["prices"]["annual"]["amount"] == 129900  # ₹1,299

    def test_institution_tiers(self, client):
        """Institution plans should have correct student limits."""
        response = client.get("/api/v1/billing/plans")
        data = response.json()
        starter = next(p for p in data["plans"] if p["id"] == "institution_starter")
        standard = next(p for p in data["plans"] if p["id"] == "institution_standard")
        premium = next(p for p in data["plans"] if p["id"] == "institution_premium")
        assert starter["max_students"] == 100
        assert standard["max_students"] == 300
        assert premium["max_students"] == 1000

    def test_plans_show_razorpay_status(self, client):
        """Plans endpoint should indicate Razorpay configuration status."""
        response = client.get("/api/v1/billing/plans")
        data = response.json()
        assert "razorpay_configured" in data


class TestSubscriptionEndpoint:
    """Subscription status endpoint tests."""

    def test_get_subscription_free_user(self, registered_user):
        """Free users should see free plan status."""
        client, _, token = registered_user
        response = client.get(
            "/api/v1/billing/subscription",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["plan"] == "free"
        assert data["is_paid"] is False
        assert data["daily_simulation_limit"] == 5

    def test_get_subscription_pro_user(self, client):
        """Pro users should see pro plan status."""
        resp = client.post("/api/v1/auth/register", json={
            "email": "prouser@test.com", "name": "Pro User",
            "password": "StrongPass123!"
        })
        token = resp.json()["access_token"]

        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "prouser@test.com").first()
        user.plan = "pro"
        db.commit()
        db.close()

        response = client.get(
            "/api/v1/billing/subscription",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["plan"] == "pro"
        assert data["is_paid"] is True
        assert data["daily_simulation_limit"] is None

    def test_get_subscription_unauthenticated(self, client):
        """Should require authentication."""
        response = client.get("/api/v1/billing/subscription")
        assert response.status_code == 401


class TestCancelEndpoint:
    """Cancel subscription endpoint tests."""

    def test_cancel_free_user_rejected(self, registered_user):
        """Free users can't cancel what they don't have."""
        client, _, token = registered_user
        response = client.post(
            "/api/v1/billing/cancel",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400


class TestCreateSubscriptionEndpoint:
    """Create subscription endpoint tests (Razorpay)."""

    def test_create_subscription_requires_auth(self, client):
        """Should require authentication."""
        response = client.post("/api/v1/billing/create-subscription", json={
            "plan": "pro", "billing_period": "monthly"
        })
        assert response.status_code == 401

    def test_create_subscription_invalid_plan(self, registered_user):
        """Should reject invalid plan names."""
        client, _, token = registered_user
        response = client.post(
            "/api/v1/billing/create-subscription",
            json={"plan": "invalid_plan", "billing_period": "monthly"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400

    def test_create_subscription_invalid_billing_period(self, registered_user):
        """Should reject invalid billing periods."""
        client, _, token = registered_user
        response = client.post(
            "/api/v1/billing/create-subscription",
            json={"plan": "pro", "billing_period": "weekly"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 400


class TestVerifyPaymentEndpoint:
    """Verify payment endpoint tests."""

    def test_verify_requires_auth(self, client):
        """Should require authentication."""
        response = client.post("/api/v1/billing/verify-payment", json={
            "razorpay_payment_id": "pay_xxx",
            "razorpay_subscription_id": "sub_xxx",
            "razorpay_signature": "sig_xxx",
        })
        assert response.status_code == 401


class TestInvoicesEndpoint:
    """Invoice endpoint tests."""

    def test_invoices_empty_for_free_user(self, registered_user):
        """Free users should have no invoices."""
        client, _, token = registered_user
        response = client.get(
            "/api/v1/billing/invoices",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["invoices"] == []
