from typing import Dict
import pytest
from sharing.share_service import create_share_link, validate_share_token, share_tokens

@pytest.fixture(autouse=True)
def cleanup_share_tokens():
    share_tokens.clear()
    yield
    share_tokens.clear()

def test_create_share_link_success():
    # Test to ensure normal usage returns a valid token and updates share_tokens
    token = create_share_link('user123', 'file456', 'read')
    assert token != ""
    assert token in share_tokens
    assert share_tokens[token]['user_id'] == 'user123'
    assert share_tokens[token]['file_id'] == 'file456'
    assert share_tokens[token]['permission_level'] == 'read'
    assert share_tokens[token]['is_valid'] is True

def test_create_share_link_mocked(monkeypatch: pytest.MonkeyPatch):
    # Test to confirm we can generate a predictable token with mocking
    monkeypatch.setattr("sharing.share_service.secrets.token_urlsafe", lambda x: "dummy_token")
    token = create_share_link('fake_user', 'fake_file', 'write')
    assert token == "dummy_token"
    assert token in share_tokens
    assert share_tokens[token]['user_id'] == 'fake_user'
    assert share_tokens[token]['file_id'] == 'fake_file'
    assert share_tokens[token]['permission_level'] == 'write'
    assert share_tokens[token]['is_valid'] is True

def test_create_share_link_with_empty_user_id():
    # Test that function handles empty user ID gracefully
    token = create_share_link('', 'file456', 'read')
    assert token != ""
    assert token in share_tokens
    assert share_tokens[token]['user_id'] == ''
    assert share_tokens[token]['file_id'] == 'file456'
    assert share_tokens[token]['permission_level'] == 'read'
    assert share_tokens[token]['is_valid'] is True

def test_create_share_link_with_empty_permission_level():
    # Test that function handles empty permission level
    token = create_share_link('user123', 'file456', '')
    assert token != ""
    assert token in share_tokens
    assert share_tokens[token]['user_id'] == 'user123'
    assert share_tokens[token]['file_id'] == 'file456'
    assert share_tokens[token]['permission_level'] == ''
    assert share_tokens[token]['is_valid'] is True

def test_validate_share_token_success():
    # Test validating a valid share token
    token = create_share_link('user123', 'file456', 'read')
    result = validate_share_token(token)
    assert result['file_id'] == 'file456'
    assert result['user_id'] == 'user123'
    assert result['permission_level'] == 'read'

def test_validate_share_token_not_found():
    # Test validating a non-existent token
    with pytest.raises(ValueError) as exc_info:
        validate_share_token("non_existent_token")
    assert "Share token does not exist." in str(exc_info.value)

def test_validate_share_token_invalid():
    # Test validating a token that has been marked invalid
    token = create_share_link('user123', 'file456', 'read')
    share_tokens[token]['is_valid'] = False
    with pytest.raises(ValueError) as exc_info:
        validate_share_token(token)
    assert "Share token is invalid." in str(exc_info.value)