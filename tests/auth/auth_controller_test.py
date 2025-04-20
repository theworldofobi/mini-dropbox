import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from config import load_config
from app import create_app
# Importing the endpoints for clarity, though we will hit them through the test client routes
from auth.auth_controller import signup_endpoint, login, logout_endpoint

@pytest.fixture
def client():
    """
    Provides a TestClient instance for making requests to the FastAPI/Flask app.
    """
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.describe("Signup Endpoint Tests")
class TestSignupEndpoint:
    @pytest.mark.it("Success Case: Should create a new user with valid data")
    @patch("auth.auth_controller.create_user")
    def test_signup_success(self, mock_create_user, client):
        """
        Test that a user can sign up successfully.
        Mock the auth_service.create_user to simulate a successful user creation.
        """
        mock_create_user.return_value = {"id": 1, "username": "test_user"}  # Simulated DB return
        payload = {"username": "test_user", "password": "test_password"}
        response = client.post("/auth/signup", json=payload)

        assert response.status_code == 201
        assert response.json()["username"] == "test_user"
        mock_create_user.assert_called_once_with("test_user", "test_password")

    @pytest.mark.it("Error Case: Should return 409 if user already exists")
    @patch("auth.auth_controller.create_user")
    def test_signup_user_exists(self, mock_create_user, client):
        """
        Test that the endpoint returns an error if the user already exists.
        The create_user function would typically raise an exception or return None for duplicates.
        """
        mock_create_user.side_effect = ValueError("User already exists")
        payload = {"username": "existing_user", "password": "some_password"}
        response = client.post("/auth/signup", json=payload)

        assert response.status_code == 409
        assert "detail" in response.json()
        mock_create_user.assert_called_once_with("existing_user", "some_password")

    @pytest.mark.it("Error Case: Should return 400 with invalid input data")
    def test_signup_invalid_data(self, client):
        """
        Test that the endpoint returns 422 if the input data is invalid or missing fields.
        """
        # Missing 'password'
        payload = {"username": "invalid_user"}
        response = client.post("/auth/signup", json=payload)

        assert response.status_code == 422
        assert "detail" in response.json()


@pytest.mark.describe("Login Endpoint Tests")
class TestLoginEndpoint:
    @pytest.mark.it("Success Case: Should authenticate a user with valid credentials")
    @patch("auth.auth_controller.verify_user")
    def test_login_success(self, mock_verify_user, client):
        """
        Test that a user can successfully log in with valid credentials.
        Mock the auth_service.verify_user to simulate a valid user record.
        """
        mock_verify_user.return_value = {"id": 2, "username": "login_test_user"}
        payload = {"username": "login_test_user", "password": "correct_password"}
        response = client.post("/auth/login", json=payload)

        assert response.status_code == 200
        assert "access_token" in response.json()
        mock_verify_user.assert_called_once_with("login_test_user", "correct_password")

    @pytest.mark.it("Error Case: Should return 401 with invalid credentials")
    @patch("auth.auth_controller.verify_user")
    def test_login_invalid_credentials(self, mock_verify_user, client):
        """
        Test that the endpoint returns 401 if the username or password is incorrect.
        Mock the auth_service.verify_user to return None or raise an exception for invalid creds.
        """
        mock_verify_user.return_value = None
        payload = {"username": "login_test_user", "password": "wrong_password"}
        response = client.post("/auth/login", json=payload)

        assert response.status_code == 401
        assert "detail" in response.json()
        mock_verify_user.assert_called_once_with("login_test_user", "wrong_password")

    @pytest.mark.it("Error Case: Should return 400 for malformed request data")
    def test_login_missing_data(self, client):
        """
        Test that the endpoint returns 422 if the request is missing username or password.
        """
        # Missing 'password'
        payload = {"username": "no_password_user"}
        response = client.post("/auth/login", json=payload)

        assert response.status_code == 422
        assert "detail" in response.json()


@pytest.mark.describe("Logout Endpoint Tests")
class TestLogoutEndpoint:
    @pytest.mark.it("Success Case: Should invalidate an active session/token")
    def test_logout_success(self, client):
        """
        Test that a user can successfully log out, invalidating their session or token.
        Typically this might require sending a valid token or session cookie.
        """
        # Assuming a token-based approach in headers
        headers = {"Authorization": "Bearer valid_token_for_user"}
        response = client.post("/auth/logout", headers=headers)

        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully"

    @pytest.mark.it("Error Case: Should return 401 if no valid session/token is provided")
    def test_logout_unauthorized(self, client):
        """
        Test that the endpoint returns 401 if the user is not authenticated or no token is provided.
        """
        response = client.post("/auth/logout")  # No headers provided
        assert response.status_code == 401
        assert "detail" in response.json()