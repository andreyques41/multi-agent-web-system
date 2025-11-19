import pytest
from app.api import create_lead, get_analytics
from app.auth import login_user

def test_main_workflow():
    # Step 1: Login user
    credentials = {"username": "admin", "password": "securepassword"}
    login_response = login_user(credentials)
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    # Step 2: Create lead
    headers = {"Authorization": f"Bearer {token}"}
    lead_data = {"name": "Jane Smith", "email": "jane.smith@example.com", "company": "BusinessCorp"}
    lead_response = create_lead(lead_data, headers=headers)
    assert lead_response.status_code == 201
    assert lead_response.json()["success"] is True

    # Step 3: Get analytics
    analytics_response = get_analytics(headers=headers)
    assert analytics_response.status_code == 200
    assert "total_leads" in analytics_response.json()
    assert "conversion_rate" in analytics_response.json()