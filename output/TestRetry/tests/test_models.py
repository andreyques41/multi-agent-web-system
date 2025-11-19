import pytest
from app.models import User, Lead

def test_user_model():
    user = User(username="admin", email="admin@example.com")
    user.set_password("securepassword")
    assert user.check_password("securepassword") is True
    assert user.check_password("wrongpassword") is False

def test_lead_model():
    lead = Lead(name="John Doe", email="john.doe@example.com", company="TestCorp")
    assert lead.name == "John Doe"
    assert lead.email == "john.doe@example.com"
    assert lead.company == "TestCorp"