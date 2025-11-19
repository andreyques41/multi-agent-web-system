import pytest
from app.auth import login_user, logout_user

def test_login_user_valid_credentials():
    credentials = {"username": "admin", "password": "securepassword"}
    response = login_user(credentials)
    assert response.status_code == 200
    assert response.json()["token"] is not None

def test_login_user_invalid_credentials():
    credentials = {"username": "admin", "password": "wrongpassword"}
    response = login_user(credentials)
    assert response.status_code == 401
    assert "error" in response.json()

def test_logout_user():
    token = "valid-auth-token"
    response = logout_user(token)
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"