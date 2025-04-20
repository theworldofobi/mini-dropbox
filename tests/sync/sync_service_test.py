from typing import Any, Dict, List
import pytest
from unittest.mock import patch, MagicMock
from sync.sync_service import get_updated_files, detect_conflicts

@pytest.mark.parametrize(
    "user_id, last_sync_ts, expected",
    [
        ("user123", 0.0, []),  # Test with timestamp 0.0 (edge case) expecting empty list
        ("user123", 1622553068.5, []),  # Test with a positive timestamp
    ]
)
def test_get_updated_files_success(user_id: str, last_sync_ts: float, expected: List[Dict[str, Any]]) -> None:
    # Since the function is not fully implemented, we currently only test that:
    # 1. It returns a List.
    # 2. It does not raise errors with valid input.
    result = get_updated_files(user_id, last_sync_ts)
    assert isinstance(result, list)
    assert result == expected

def test_get_updated_files_invalid_user_id() -> None:
    # Test that ValueError is raised when the user_id is empty
    with pytest.raises(ValueError) as exc:
        get_updated_files("", 1622553068.5)
    assert "User ID cannot be empty." in str(exc.value)

def test_get_updated_files_negative_timestamp() -> None:
    # Test that ValueError is raised when the timestamp is negative
    with pytest.raises(ValueError) as exc:
        get_updated_files("user123", -1.0)
    assert "Timestamp cannot be negative." in str(exc.value)

def test_detect_conflicts_same_version() -> None:
    # Test when both versions are the same
    local = {"version": 1, "content": "local_content"}
    remote = {"version": 1, "content": "remote_content"}
    result = detect_conflicts(local, remote)
    assert result == local

def test_detect_conflicts_conflict() -> None:
    # Test when there is a conflict (different version numbers)
    local = {"version": 2, "content": "local_content"}
    remote = {"version": 3, "content": "remote_content"}
    result = detect_conflicts(local, remote)
    assert result["version"] == 3
    assert "content" in result
    assert result["content"] == "merged_content"

def test_detect_conflicts_missing_version() -> None:
    # Test that KeyError is raised when 'version' is missing
    local = {"content": "local_content"}
    remote = {"version": 2, "content": "remote_content"}
    with pytest.raises(KeyError) as exc:
        detect_conflicts(local, remote)
    assert "Missing 'version' key" in str(exc.value)