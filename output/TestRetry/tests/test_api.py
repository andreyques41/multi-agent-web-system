import pytest
from app.api import create_lead, get_analytics

def test_create_lead_valid_data():
    data = {"name": "John Doe", "email": "john.doe@example.com", "company": "TestCorp"}
    response = create_lead(data)
    assert response.status_code == 201
    assert response.json()["success"] is True

def test_create_lead_invalid_data():
    data = {"name": "", "email": "invalid-email", "company": ""}
    response = create_lead(data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_get_analytics():
    response = get_analytics()
    assert response.status_code == 200
    assert "total_leads" in response.json()
    assert "conversion_rate" in response.json()