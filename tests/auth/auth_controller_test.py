from typing import Dict
import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from auth.auth_controller import router, UserCredentials


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_signup_endpoint_success(client):
    response = client.post("/auth/signup", json={"username": "newuser", "password": "newpass"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"


def test_signup_endpoint_error(client):
    with patch("auth.auth_controller.signup_endpoint", side_effect=HTTPException(status_code=400, detail="Creation error")):
        response = client.post("/auth/signup", json={"username": "baduser", "password": "badpass"})
        assert response.status_code == 400
        assert response.json()["detail"] == "Creation error"


def test_login_endpoint_success(client):
    response = client.post("/auth/login", json={"username": "validuser", "password": "validpass"})
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_endpoint_error(client):
    with patch("auth.auth_controller.login_endpoint", side_effect=HTTPException(status_code=401, detail="Invalid credentials")):
        response = client.post("/auth/login", json={"username": "invaliduser", "password": "wrongpass"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"


def test_logout_endpoint_success(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"


def test_logout_endpoint_error(client):
    with patch("auth.auth_controller.logout_endpoint", side_effect=HTTPException(status_code=400, detail="Logout error")):
        response = client.post("/auth/logout")
        assert response.status_code == 400
        assert response.json()["detail"] == "Logout error"