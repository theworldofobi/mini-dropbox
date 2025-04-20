from typing import Any
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import create_app, run_app

def test_create_app_success() -> None:
    # Tests that create_app returns a Flask instance and the health endpoint works
    app = create_app()
    assert isinstance(app, Flask)
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json == {"status": "OK"}

def test_create_app_exception() -> None:
    # Tests that create_app raises a RuntimeError when Flask initialization fails
    with patch("app.Flask", side_effect=Exception("Mock Error")):
        with pytest.raises(RuntimeError) as exc_info:
            create_app()
        assert "Failed to create Flask application: Mock Error" in str(exc_info.value)

def test_run_app_success() -> None:
    # Tests that run_app calls Flask's run() with the correct arguments
    mock_app = MagicMock()
    with patch("app.create_app", return_value=mock_app):
        run_app(port=6000)
        mock_app.run.assert_called_once_with(host="0.0.0.0", port=6000)

def test_run_app_exception_from_create_app() -> None:
    # Tests that run_app raises a RuntimeError if create_app fails
    with patch("app.create_app", side_effect=RuntimeError("Mock create_app error")):
        with pytest.raises(RuntimeError) as exc_info:
            run_app(port=5001)
        assert "Failed to start Flask server: Mock create_app error" in str(exc_info.value)

def test_run_app_exception_from_app_run() -> None:
    # Tests that run_app raises a RuntimeError if app.run() fails
    mock_app = MagicMock()
    mock_app.run.side_effect = Exception("Mock run error")
    with patch("app.create_app", return_value=mock_app):
        with pytest.raises(RuntimeError) as exc_info:
            run_app(port=5002)
        assert "Failed to start Flask server: Mock run error" in str(exc_info.value)