from typing import Any
import pytest
from flask import Flask
from unittest.mock import patch
from examples.basic_sync_demo.demo_app import init_demo_app, demo_upload_file, demo_sync_cycle

@pytest.fixture
def app() -> Flask:
    return init_demo_app()

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_init_demo_app_returns_flask_instance():
    application = init_demo_app()
    assert isinstance(application, Flask)

def test_init_demo_app_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Demo App is running." in response.data

def test_demo_upload_file_success():
    with patch("examples.basic_sync_demo.demo_app.logging.info") as mock_log:
        demo_upload_file()
        mock_log.assert_any_call("Starting demo file upload.")
        mock_log.assert_any_call("File upload completed successfully.")

def test_demo_upload_file_error():
    with patch("examples.basic_sync_demo.demo_app.logging.info", side_effect=Exception("Upload error")):
        with pytest.raises(Exception) as excinfo:
            demo_upload_file()
        assert "Upload error" in str(excinfo.value)

def test_demo_sync_cycle_success():
    with patch("examples.basic_sync_demo.demo_app.logging.info") as mock_log:
        demo_sync_cycle()
        mock_log.assert_any_call("Starting demo sync cycle.")
        mock_log.assert_any_call("Sync cycle completed successfully.")

def test_demo_sync_cycle_error():
    with patch("examples.basic_sync_demo.demo_app.logging.info", side_effect=Exception("Sync error")):
        with pytest.raises(Exception) as excinfo:
            demo_sync_cycle()
        assert "Sync error" in str(excinfo.value)