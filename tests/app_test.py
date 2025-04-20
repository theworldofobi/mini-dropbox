import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the functions we want to test from app.py
from app import create_app, run_app

@pytest.fixture
def client():
    """
    Fixture that creates a TestClient instance using the FastAPI/Flask 
    application returned by create_app().
    """
    test_app = create_app()
    return TestClient(test_app)

def test_create_app_returns_valid_app(client):
    """
    Test that create_app() returns a valid application instance 
    that can be used with TestClient.
    """
    # A simple GET request to a non-existing route should return a 404, 
    # indicating the app is running and callable
    response = client.get("/unknown_route")
    assert response.status_code == 404, "Expected 404 for unknown route, got a different status code."

def test_create_app_registers_routes(client):
    """
    Test that create_app() registers at least one route or endpoint.
    This checks that blueprints/routers are successfully attached.
    """
    # FastAPI: Check if there are any routes attached
    # Flask: This might differ, but for demonstration, we assume FastAPI style
    app_routes = client.app.routes
    assert len(app_routes) > 0, "No routes were registered in the application."

def test_run_app_starts_server_successfully():
    """
    Test that run_app() attempts to start the server successfully 
    by mocking the underlying server call.
    """
    with patch("app.uvicorn.run") as mock_run:
        run_app()
        mock_run.assert_called_once()
        # Optionally check the port or other parameters passed to uvicorn.run
        # e.g., mock_run.assert_called_with("app:create_app", host="0.0.0.0", port=8000, log_level="info")

def test_run_app_with_custom_port():
    """
    Test run_app() with a custom port to ensure it starts on the specified port.
    """
    with patch("app.uvicorn.run") as mock_run:
        run_app(port=5001)
        # Verify run was called with port=5001
        mock_run.assert_called_once()
        _, kwargs = mock_run.call_args
        assert kwargs.get("port") == 5001, "run_app did not receive the custom port as expected."

def test_run_app_raises_exception_on_error():
    """
    Test run_app() behavior when the underlying server call raises an exception.
    Ensures that the function does not silently swallow errors.
    """
    with patch("app.uvicorn.run", side_effect=Exception("Server Error")) as mock_run:
        with pytest.raises(Exception) as exc_info:
            run_app()
        assert "Server Error" in str(exc_info.value), "Expected 'Server Error' exception not raised."
        mock_run.assert_called_once()