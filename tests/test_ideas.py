"""Test ideas generation endpoint"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@patch('app.services.ai_service.generate_ideas')
def test_generate_ideas_success(mock_generate, client):
    """Test successful ideas generation"""
    # Mock the generate_ideas function
    mock_ideas = [
        "AI Trends in 2024",
        "Machine Learning Best Practices",
        "Deep Learning Architectures",
        "Neural Networks Explained",
        "Computer Vision Applications"
    ]
    mock_generate.return_value = mock_ideas
    
    payload = {
        "topic": "Artificial Intelligence",
        "audience": "Tech Developers",
        "tone": "Technical",
        "count": 5
    }
    
    response = client.post("/api/ideas/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Artificial Intelligence"
    assert data["audience"] == "Tech Developers"
    assert len(data["ideas"]) == 5
    assert data["ideas"] == mock_ideas


@patch('app.services.ai_service.generate_ideas')
def test_generate_ideas_invalid_count(mock_generate, client):
    """Test ideas generation with invalid count"""
    payload = {
        "topic": "Technology",
        "audience": "General",
        "tone": "Professional",
        "count": 100  # Exceeds max of 20
    }
    
    response = client.post("/api/ideas/generate", json=payload)
    assert response.status_code == 422  # Validation error


@patch('app.services.ai_service.generate_ideas')
def test_generate_ideas_missing_topic(mock_generate, client):
    """Test ideas generation with missing required field"""
    payload = {
        "audience": "Tech",
        "tone": "Casual",
        "count": 5
    }
    
    response = client.post("/api/ideas/generate", json=payload)
    assert response.status_code == 422  # Validation error
