"""
Unit tests for authentication API
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_login_success():
    """Test successful login"""
    response = client.post(
        "/auth/token",
        data={
            "username": "demo",
            "password": "demopassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/token",
        data={
            "username": "invalid",
            "password": "wrong"
        }
    )
    
    assert response.status_code == 401


def test_register_new_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_register_duplicate_user():
    """Test registration with existing username"""
    # First registration
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup@example.com",
            "password": "password123"
        }
    )
    
    # Second registration with same username
    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "dup2@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400


def test_get_current_user():
    """Test getting current user profile"""
    # Login first
    login_response = client.post(
        "/auth/token",
        data={
            "username": "demo",
            "password": "demopassword"
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Get user profile
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["username"] == "demo"


def test_invalid_token():
    """Test request with invalid token"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    
    assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
