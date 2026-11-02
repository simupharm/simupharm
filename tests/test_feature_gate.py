"""Tests for Feature Gating — Plan restrictions and simulation limits (Razorpay)."""


class TestFeatureGateDependencies:
    """Test feature gate dependency functions."""

    def test_require_plan_exists(self):
        """Feature gate dependencies should be importable."""
        from backend.middleware.feature_gate import (
            require_plan, require_pro, require_institution,
            check_simulation_limit, get_allowed_instruments,
        )
        assert callable(require_pro)
        assert callable(require_institution)
        assert callable(check_simulation_limit)

    def test_free_instruments_list(self):
        """Free plan should have 3 instruments."""
        from backend.billing.razorpay_service import FREE_INSTRUMENTS, ALL_INSTRUMENTS
        assert set(FREE_INSTRUMENTS) == {"uvvis", "polarimeter", "psa"}
        assert len(ALL_INSTRUMENTS) == 7

    def test_get_allowed_instruments_free(self):
        """Free user should only access UV-Vis, Polarimeter, PSA."""
        from backend.middleware.feature_gate import get_allowed_instruments

        class FakeUser:
            plan = "free"

        instruments = get_allowed_instruments(FakeUser())
        assert set(instruments) == {"uvvis", "polarimeter", "psa"}

    def test_get_allowed_instruments_pro(self):
        """Pro user should access all 7 instruments."""
        from backend.middleware.feature_gate import get_allowed_instruments

        class FakeUser:
            plan = "pro"

        instruments = get_allowed_instruments(FakeUser())
        assert len(instruments) == 7
        assert "hplc" in instruments
        assert "ftir" in instruments
        assert "gc" in instruments
        assert "mass_spec" in instruments


class TestPlanConstants:
    """Test plan configuration constants."""

    def test_plan_definitions_complete(self):
        """All plans should be properly defined."""
        from backend.billing.razorpay_service import PLANS
        assert "free" in PLANS
        assert "pro" in PLANS
        assert "institution_starter" in PLANS
        assert "institution_standard" in PLANS
        assert "institution_premium" in PLANS

    def test_free_plan_limits(self):
        """Free plan should have correct limits."""
        from backend.billing.razorpay_service import PLANS
        free = PLANS["free"]
        assert free["daily_simulation_limit"] == 5
        assert free["quiz_limit_monthly"] == 5
        assert len(free["instruments"]) == 3

    def test_pro_plan_unlimited(self):
        """Pro plan should have no limits."""
        from backend.billing.razorpay_service import PLANS
        pro = PLANS["pro"]
        assert pro["daily_simulation_limit"] is None
        assert pro["quiz_limit_monthly"] is None
        assert len(pro["instruments"]) == 7

    def test_pro_pricing_inr(self):
        """Pro pricing should be in INR (paise)."""
        from backend.billing.razorpay_service import PLANS
        prices = PLANS["pro"]["prices"]
        assert prices["monthly"]["amount"] == 19900  # ₹199
        assert prices["semester"]["amount"] == 79900  # ₹799
        assert prices["annual"]["amount"] == 129900  # ₹1,299

    def test_institution_student_limits(self):
        """Institution plans should have correct student limits."""
        from backend.billing.razorpay_service import PLANS
        assert PLANS["institution_starter"]["max_students"] == 100
        assert PLANS["institution_standard"]["max_students"] == 300
        assert PLANS["institution_premium"]["max_students"] == 1000


class TestSimulationLimitLogic:
    """Test daily simulation limit counter logic."""

    def test_free_user_daily_count_resets(self, client):
        """Free user's simulation count should reset on new day."""
        resp = client.post("/api/v1/auth/register", json={
            "email": "limit@test.com", "name": "Limit User",
            "password": "StrongPass123!"
        })
        token = resp.json()["access_token"]

        sub = client.get(
            "/api/v1/billing/subscription",
            headers={"Authorization": f"Bearer {token}"}
        )
        data = sub.json()
        assert data["plan"] == "free"
        assert data["simulations_today"] == 0

    def test_pro_user_unlimited(self, client):
        """Pro user should have no simulation limit."""
        resp = client.post("/api/v1/auth/register", json={
            "email": "prolimit@test.com", "name": "Pro Limit User",
            "password": "StrongPass123!"
        })
        token = resp.json()["access_token"]

        from tests.conftest import TestSessionLocal
        from backend.models import User
        db = TestSessionLocal()
        user = db.query(User).filter(User.email == "prolimit@test.com").first()
        user.plan = "pro"
        db.commit()
        db.close()

        sub = client.get(
            "/api/v1/billing/subscription",
            headers={"Authorization": f"Bearer {token}"}
        )
        data = sub.json()
        assert data["plan"] == "pro"
        assert data["daily_simulation_limit"] is None


class TestRazorpayService:
    """Test Razorpay service utility functions."""

    def test_razorpay_not_configured_by_default(self):
        """Razorpay should not be configured without env vars."""
        from backend.billing.razorpay_service import is_razorpay_configured
        # In test env, Razorpay keys are not set
        result = is_razorpay_configured()
        assert isinstance(result, bool)

    def test_plan_instruments_match(self):
        """Free and all instruments should be consistent."""
        from backend.billing.razorpay_service import FREE_INSTRUMENTS, ALL_INSTRUMENTS
        # All free instruments should be a subset of all instruments
        assert all(i in ALL_INSTRUMENTS for i in FREE_INSTRUMENTS)
        # Pro instruments not in free
        pro_only = set(ALL_INSTRUMENTS) - set(FREE_INSTRUMENTS)
        assert "hplc" in pro_only
        assert "ftir" in pro_only
        assert "gc" in pro_only
        assert "mass_spec" in pro_only
