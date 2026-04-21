"""Tests for API documentation endpoints."""


def test_health_check(client):
    """Health endpoint should remain available."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_offline_redoc_available(client):
    """Offline ReDoc fallback should render without external dependencies."""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "Football Analytics API" in response.text
    assert "/openapi.json" in response.text
    assert "Sections" in response.text

