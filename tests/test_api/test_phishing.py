"""
Unit tests for phishing detection API
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_phishing_scan_valid_url():
    """Test phishing scan with valid URL"""
    response = client.post(
        "/scan/phishing",
        json={
            "url": "https://example.com",
            "capture_screenshot": True,
            "analyze_dom": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "scan_id" in data
    assert "verdict" in data
    assert "risk_score" in data
    assert data["verdict"] in ["PHISH", "LEGITIMATE"]
    assert 0 <= data["risk_score"] <= 1


def test_phishing_scan_invalid_url():
    """Test phishing scan with invalid URL"""
    response = client.post(
        "/scan/phishing",
        json={
            "url": "not-a-valid-url",
            "capture_screenshot": True,
            "analyze_dom": True
        }
    )
    
    # Should fail validation
    assert response.status_code == 422


def test_bulk_scan():
    """Test bulk phishing scan"""
    response = client.post(
        "/scan/phishing/bulk",
        json={
            "urls": [
                "https://example1.com",
                "https://example2.com",
                "https://example3.com"
            ]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "task_id" in data
    assert data["total_urls"] == 3


def test_rate_limiting():
    """Test rate limiting middleware"""
    # Make multiple requests rapidly
    responses = []
    for _ in range(5):
        response = client.post(
            "/scan/phishing",
            json={
                "url": "https://example.com",
                "capture_screenshot": False,
                "analyze_dom": False
            }
        )
        responses.append(response)
    
    # All should succeed within rate limit
    assert all(r.status_code == 200 for r in responses)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
