import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from app import create_app
from fastapi import Depends
from auth.auth_service import get_current_user

"""
Tests for sync/sync_controller.py

Functions:
1. init_sync_endpoint(request) - Called when a client starts syncing; 
   returns changed files since last sync
2. resolve_conflict_endpoint(request) - Allows a user to pick a version 
   if there's a conflict
"""

@pytest.fixture(scope="module")
def client():
    """
    Fixture to create a TestClient for the FastAPI application.
    """
    app = create_app()
    
    # Create a test user
    test_user = {"id": "test_user_id", "email": "test@example.com"}
    
    # Override the app's dependency with our own test version
    app.dependency_overrides[get_current_user] = lambda: test_user
    
    test_client = TestClient(app)
    yield test_client
    
    # Clean up after tests
    app.dependency_overrides.clear()

@pytest.mark.describe("init_sync_endpoint() Tests")
class TestInitSyncEndpoint:

    @pytest.mark.it("Successfully returns updated files when provided with valid data")
    @patch("sync.sync_service.get_updated_files")
    def test_init_sync_endpoint_success(self, mock_get_updated_files, client):
        """
        Test that a valid request with a proper last_sync_ts and 
        authenticated user returns a list of updated files.
        """
        # Mock the service function return value
        mock_get_updated_files.return_value = [
            {"file_id": "file123", "last_modified": "2023-10-10T12:00:00Z"}
        ]

        # Send last_sync_ts as a query parameter, not in the JSON body
        response = client.post(
            "/sync/init?last_sync_ts=1633867200.0"  # Providing as query param
        )

        # Assertions
        assert response.status_code == 200, "Expected 200 OK on success"
        data = response.json()
        assert "changed_files" in data, "Response should contain 'changed_files' key"
        assert data["changed_files"] == [
            {"file_id": "file123", "last_modified": "2023-10-10T12:00:00Z"}
        ], "Should return the mocked list of updated files"
        assert "current_timestamp" in data, "Response should include current_timestamp"
        mock_get_updated_files.assert_called_once_with(
            user_id="test_user_id",
            last_sync_ts=1633867200.0
        )

    @pytest.mark.it("Returns error if last_sync_ts is missing from request")
    def test_init_sync_endpoint_missing_last_sync_ts(self, client):
        """
        Test that the endpoint returns an error or 400 status 
        when the request is missing required parameter(s).
        """
        # The endpoint expects last_sync_ts as a query parameter, not in the JSON body
        response = client.post("/sync/init")
        assert response.status_code == 422, "Expected 422 Unprocessable Entity when parameter is missing"


@pytest.mark.describe("resolve_conflict_endpoint() Tests")
class TestResolveConflictEndpoint:

    @pytest.mark.it("Successfully resolves a conflict when provided with valid data")
    @patch("sync.sync_service.detect_conflicts")
    def test_resolve_conflict_endpoint_success(self, mock_detect_conflicts, client):
        """
        Test that a valid request containing local and remote version 
        details allows a conflict to be resolved successfully.
        """
        # Mock the conflict detection to signal a conflict
        mock_detect_conflicts.return_value = {
            "conflict": True,
            "merged_data": "remote_wins"
        }

        # Prepare request data per the actual controller implementation
        request_body = {
            "local_version": {"file_id": "abc", "content": "local"},
            "remote_version": {"file_id": "abc", "content": "remote"}
        }

        response = client.post("/sync/resolve", json=request_body)
        assert response.status_code == 200, "Expected 200 OK on successful resolution"
        data = response.json()

        # Validate response structure according to actual controller implementation
        assert "resolved_version" in data, "Response should contain resolved_version"
        assert data["resolved_version"] == {
            "conflict": True,
            "merged_data": "remote_wins"
        }, "Expected proper resolution data"
        assert "timestamp" in data, "Response should include timestamp"
        mock_detect_conflicts.assert_called_once_with(
            {"file_id": "abc", "content": "local"}, 
            {"file_id": "abc", "content": "remote"}
        )

    @pytest.mark.it("Returns error when there is an invalid request")
    @patch("sync.sync_service.detect_conflicts")
    def test_resolve_conflict_endpoint_error(self, mock_detect_conflicts, client):
        """
        Test that the endpoint handles errors properly.
        """
        # Mock the conflict detection to raise an error
        mock_detect_conflicts.side_effect = ValueError("Invalid file versions provided")

        request_body = {
            "local_version": {"file_id": "abc", "content": "local"},
            "remote_version": {"file_id": "def", "content": "remote"}  # Different file IDs
        }

        response = client.post("/sync/resolve", json=request_body)
        assert response.status_code == 400, "Expected 400 Bad Request when error occurs"
        data = response.json()
        assert "detail" in data, "Expected 'detail' field in the error response"
        assert "Invalid file versions" in data["detail"], "Error message should be returned"