"""Tests for /api/health endpoint."""


def test_health_check(client):
    """Health endpoint should return status and engine list."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "SimuPharma API"
    assert "uvvis" in data["engines"]
    assert "ftir" in data["engines"]
    assert "hplc" in data["engines"]
    assert "gc" in data["engines"]
    assert "mass_spec" in data["engines"]
    assert "polarimeter" in data["engines"]
    assert "psa" in data["engines"]
    assert data["ai"]["autonomous_agent"] is True
    assert data["ai"]["adaptive_learning"] is True
    assert "environment" in data
