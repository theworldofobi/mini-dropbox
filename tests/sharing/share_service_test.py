import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from sharing.share_service import create_share_link, validate_share_token, revoke_share_link, share_tokens

@pytest.fixture
def mock_user_id():
    """Fixture for a valid user ID."""
    return "123"

@pytest.fixture
def mock_file_id():
    """Fixture for a valid file ID."""
    return "456"

@pytest.fixture
def mock_permission_level():
    """Fixture for a valid permission level."""
    return "read"

@pytest.fixture
def mock_token():
    """Fixture for a valid share token."""
    return "valid_share_token_abc123"

@pytest.fixture
def mock_share_data():
    """Fixture for sample share data."""
    return {
        "token": "valid_share_token_abc123",
        "user_id": "123",
        "file_id": "456",
        "permission_level": "read",
        "is_valid": True,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(days=7),
        "access_count": 0
    }

@pytest.fixture
def setup_mock_share_token(mock_token, mock_share_data):
    """Setup a mock share token in the share_tokens dictionary."""
    share_tokens[mock_token] = mock_share_data
    yield
    # Clean up
    if mock_token in share_tokens:
        del share_tokens[mock_token]


# --------------------------------------------------------
# Tests for create_share_link
# --------------------------------------------------------

def test_create_share_link_valid(mock_user_id, mock_file_id, mock_permission_level):
    """
    Test creating a share link with valid inputs.
    Expects a non-empty token or link that indicates success.
    """
    with patch("sharing.share_service.secrets.token_urlsafe", return_value="test_token"):
        result = create_share_link(
            user_id=mock_user_id, 
            file_id=mock_file_id, 
            permission_level=mock_permission_level
        )
        
        # Verify the result is not None or empty
        assert result is not None, "Expected a valid share link data"
        assert isinstance(result, dict), "Share link data should be a dictionary"
        assert result["token"] == "test_token"
        assert result["file_id"] == mock_file_id
        assert result["user_id"] == mock_user_id
        assert result["permission_level"] == mock_permission_level


def test_create_share_link_invalid_user():
    """
    Test creating a share link with null user ID.
    Verifies that the function still works but records the null user.
    """
    invalid_user_id = None  # Simulate missing user
    mock_file_id = "456"
    
    # No exception is raised, just check the result
    result = create_share_link(
        user_id=invalid_user_id, 
        file_id=mock_file_id, 
        permission_level="read"
    )
    
    # Verify the result contains the null user_id
    assert result is not None
    assert result["user_id"] is None
    assert result["file_id"] == mock_file_id


# --------------------------------------------------------
# Tests for validate_share_token
# --------------------------------------------------------

def test_validate_share_token_valid(mock_token, setup_mock_share_token):
    """
    Test validating a token that is known to be valid.
    Expects to return associated file/user info or data without error.
    """
    validation_result = validate_share_token(mock_token)
    
    assert validation_result is not None, "Expected validation result for a valid token"
    assert validation_result["file_id"] == "456"
    assert validation_result["user_id"] == "123"
    assert validation_result["access_count"] == 1, "Access count should be incremented"


def test_validate_share_token_invalid():
    """
    Test validating an invalid/expired token.
    Expects an exception or error result.
    """
    invalid_token = "nonexistent_token"
    
    with pytest.raises(ValueError, match="Share token does not exist"):
        validate_share_token(invalid_token)


def test_validate_share_token_expired(mock_token):
    """
    Test validating an expired token.
    """
    # Create expired token
    expired_data = {
        "token": mock_token,
        "user_id": "123",
        "file_id": "456",
        "permission_level": "read",
        "is_valid": True,
        "created_at": datetime.utcnow() - timedelta(days=10),
        "expires_at": datetime.utcnow() - timedelta(days=3),  # Expired 3 days ago
        "access_count": 0
    }
    
    share_tokens[mock_token] = expired_data
    
    try:
        with pytest.raises(ValueError, match="Share token has expired"):
            validate_share_token(mock_token)
    finally:
        # Clean up
        if mock_token in share_tokens:
            del share_tokens[mock_token]


# --------------------------------------------------------
# Tests for revoke_share_link
# --------------------------------------------------------

def test_revoke_share_link_success(mock_token, setup_mock_share_token):
    """
    Test successful revocation of a share link.
    """
    # Get the user_id from the mock data
    user_id = share_tokens[mock_token]["user_id"]
    
    # Revoke the token
    revoke_share_link(mock_token, user_id)
    
    # Verify token is no longer valid
    assert share_tokens[mock_token]["is_valid"] == False, "Token should be marked as invalid"


def test_revoke_share_link_unauthorized(mock_token, setup_mock_share_token):
    """
    Test unauthorized revocation attempt.
    """
    wrong_user_id = "wrong_user"
    
    with pytest.raises(ValueError, match="Unauthorized to revoke this share link"):
        revoke_share_link(mock_token, wrong_user_id)