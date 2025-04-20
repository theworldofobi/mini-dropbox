import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta

# Import from the project root
from sync.sync_service import get_updated_files, detect_conflicts
from files.file_service import _file_db  # This is what sync_service actually uses


@pytest.fixture
def mock_file_db():
    """
    Fixture to set up and tear down a mock file database.
    """
    # Save original 
    original_db = _file_db.copy()
    
    # Clear for testing
    _file_db.clear()
    
    yield _file_db
    
    # Restore original
    _file_db.clear()
    _file_db.update(original_db)


@pytest.fixture
def mock_timestamp():
    """Fixture to provide a baseline timestamp for testing."""
    return datetime.now(timezone.utc).timestamp() - 86400  # 1 day ago


@pytest.fixture
def mock_user_id():
    """Fixture to provide a sample user ID for testing."""
    return "123"


def test_get_updated_files_returns_correct_files(mock_file_db, mock_user_id, mock_timestamp):
    """
    Test that get_updated_files returns the correct files that were 
    updated after the given timestamp.
    """
    # Add some test files to the mock database
    one_hour_ago = datetime.now() - timedelta(hours=1)
    two_days_ago = datetime.now() - timedelta(days=2)
    
    # File updated after the timestamp
    mock_file_db["file1"] = {
        "file_id": "file1",
        "user_id": mock_user_id,
        "updated_at": one_hour_ago
    }
    
    # File updated before the timestamp
    mock_file_db["file2"] = {
        "file_id": "file2",
        "user_id": mock_user_id,
        "updated_at": two_days_ago
    }
    
    # File from different user
    mock_file_db["file3"] = {
        "file_id": "file3",
        "user_id": "different_user",
        "updated_at": one_hour_ago
    }
    
    # Get updated files
    result = get_updated_files(mock_user_id, mock_timestamp)
    
    # Should only contain file1 (updated after timestamp and belongs to the user)
    assert len(result) == 1
    assert result[0]["file_id"] == "file1"


def test_get_updated_files_handles_empty_db(mock_file_db, mock_user_id, mock_timestamp):
    """Test that get_updated_files handles an empty database correctly."""
    # Database is already cleared by the fixture
    
    result = get_updated_files(mock_user_id, mock_timestamp)
    assert len(result) == 0, "Should return empty list when no files are in the database"


def test_get_updated_files_invalid_user_id():
    """
    Test that get_updated_files raises a ValueError when the user_id is invalid.
    """
    with pytest.raises(ValueError, match="User ID cannot be empty"):
        get_updated_files("", 1234567890.0)


def test_get_updated_files_invalid_timestamp(mock_user_id):
    """
    Test that get_updated_files raises a ValueError when the timestamp is invalid.
    """
    with pytest.raises(ValueError, match="Timestamp cannot be negative"):
        get_updated_files(mock_user_id, -1.0)


def test_detect_conflicts_no_conflict():
    """
    Test that detect_conflicts returns the local version when versions match.
    """
    local_version = {"file_id": 1, "version": 5, "content": "abc123"}
    remote_version = {"file_id": 1, "version": 5, "content": "abc123"}

    result = detect_conflicts(local_version, remote_version)
    assert result == local_version, "Expected local version to be returned when no conflict"


def test_detect_conflicts_local_newer():
    """
    Test that detect_conflicts keeps local version when the local modified time is newer.
    """
    local_version = {
        "file_id": 1, 
        "version": 5, 
        "content": "local-changes",
        "modified_at": datetime.now()
    }
    remote_version = {
        "file_id": 1, 
        "version": 6, 
        "content": "remote-changes",
        "modified_at": datetime.now() - timedelta(hours=1)
    }

    result = detect_conflicts(local_version, remote_version)
    assert "conflict_status" in result, "Expected conflict_status in the result"
    assert result["conflict_status"] == "resolved_keep_local", "Expected to keep local version"
    assert result["conflicting_version"] == 6, "Expected to record remote version as conflicting"


def test_detect_conflicts_remote_newer():
    """
    Test that detect_conflicts keeps remote version when the remote modified time is newer.
    """
    local_version = {
        "file_id": 1, 
        "version": 5, 
        "content": "local-changes",
        "modified_at": datetime.now() - timedelta(hours=1)
    }
    remote_version = {
        "file_id": 1, 
        "version": 6, 
        "content": "remote-changes",
        "modified_at": datetime.now()
    }

    result = detect_conflicts(local_version, remote_version)
    assert "conflict_status" in result, "Expected conflict_status in the result"
    assert result["conflict_status"] == "resolved_keep_remote", "Expected to keep remote version"
    assert result["conflicting_version"] == 5, "Expected to record local version as conflicting"


def test_detect_conflicts_missing_version_key():
    """
    Test detect_conflicts raises KeyError when version key is missing.
    """
    local_version = {"file_id": 1, "content": "local"}  # Missing version key
    remote_version = {"file_id": 1, "version": 2, "content": "remote"}

    with pytest.raises(KeyError, match="Missing 'version' key in version data"):
        detect_conflicts(local_version, remote_version)


def test_detect_conflicts_none_value():
    """
    Test detect_conflicts handles None values appropriately.
    """
    local_version = {"file_id": 1, "version": 5, "content": "local"}
    remote_version = None

    with pytest.raises(TypeError):
        detect_conflicts(local_version, remote_version)