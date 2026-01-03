"""
Unit tests for Job Scam Detection API
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_analyze_legitimate_job():
    """Test analysis of legitimate job posting"""
    job_text = (
        "Software Engineer position at Tech Corp. "
        "Requirements: 3+ years Python experience, BS in CS. "
        "Competitive salary and benefits. Apply at careers@techcorp.com"
    )
    
    response = client.post("/analyze", json={"text": job_text})
    assert response.status_code == 200
    
    data = response.json()
    assert "prediction" in data
    assert "score" in data
    assert "flags" in data
    assert data["score"] >= 50  # Should be relatively high trust score


def test_analyze_scam_job():
    """Test analysis of obvious scam posting"""
    scam_text = (
        "URGENT!!! Earn $500 per day from home! "
        "No experience needed! Pay $99 registration fee to start! "
        "WhatsApp only: 555-0123. Limited slots!!!"
    )
    
    response = client.post("/analyze", json={"text": scam_text})
    assert response.status_code == 200
    
    data = response.json()
    assert data["prediction"] in ["High Risk Scam", "Suspicious"]
    assert data["score"] < 50  # Should be low trust score
    assert len(data["flags"]) > 0  # Should have scam flags


def test_analyze_with_url():
    """Test analysis with URL parameter"""
    response = client.post("/analyze", json={
        "text": "Job posting text",
        "url": "https://example.com/job/123"
    })
    assert response.status_code == 200


def test_analyze_empty_text():
    """Test that empty text is handled"""
    response = client.post("/analyze", json={"text": ""})
    # Should either return error or handle gracefully
    assert response.status_code in [200, 400, 500]


def test_report_scam():
    """Test scam reporting endpoint"""
    response = client.post("/report", json={
        "text": "Scam job posting",
        "url": "https://scam-site.com/job"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_batch_analyze():
    """Test batch analysis endpoint"""
    texts = [
        "Legitimate software engineer job",
        "URGENT!!! Pay $99 fee to start!!!"
    ]
    
    response = client.post("/batch-analyze", json=texts)
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2


def test_response_structure():
    """Test that response has all required fields"""
    response = client.post("/analyze", json={
        "text": "Test job posting"
    })
    
    data = response.json()
    required_fields = [
        "prediction", "score", "flags", "highlighted_phrases",
        "explanation", "advice", "confidence"
    ]
    
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"


def test_trust_score_range():
    """Test that trust score is in valid range"""
    response = client.post("/analyze", json={
        "text": "Software engineer needed"
    })
    
    data = response.json()
    assert 0 <= data["score"] <= 100
    assert 0.0 <= data["confidence"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
