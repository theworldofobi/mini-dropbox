from typing import Any, Dict
import pytest
from sharing.share_controller import create_share_link_endpoint, revoke_share_link_endpoint

def test_create_share_link_endpoint_valid_file_id():
    # Tests whether the function returns the expected dictionary for a valid file_id
    file_id = "test_file_id"
    result = create_share_link_endpoint(file_id)
    assert isinstance(result, dict)
    assert "share_id" in result
    assert "share_link" in result
    assert "file_id" in result
    assert result["file_id"] == file_id

def test_create_share_link_endpoint_raises_value_error_on_exception(mocker):
    # Tests whether a ValueError is raised if an internal error occurs
    mocker.patch("sharing.share_controller.create_share_link_endpoint", side_effect=Exception("Test error"))
    with pytest.raises(ValueError) as exc:
        create_share_link_endpoint("any_id")
    assert "Failed to create share link: Test error" in str(exc.value)

def test_revoke_share_link_endpoint_valid_id():
    # Tests whether the function completes without error for a valid share_id
    try:
        revoke_share_link_endpoint("valid_share_id")
    except Exception as exc:
        pytest.fail(f"Unexpected exception raised: {exc}")

def test_revoke_share_link_endpoint_invalid_id():
    # Tests whether a ValueError is raised for an invalid share_id
    with pytest.raises(ValueError) as exc:
        revoke_share_link_endpoint("")
    assert "Invalid share_id provided." in str(exc.value)