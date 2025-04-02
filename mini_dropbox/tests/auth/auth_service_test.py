from typing import Dict, Any
import pytest
import bcrypt
from auth.auth_service import create_user, verify_user

@pytest.fixture
def reset_mock_db():
    from auth.auth_service import _mock_db
    _mock_db.clear()
    yield
    _mock_db.clear()

def test_create_user_success(reset_mock_db):
    user_data = create_user("john_doe", "securePass123")
    assert user_data["username"] == "john_doe"
    assert isinstance(user_data["id"], int)

def test_create_user_existing_user(reset_mock_db):
    create_user("john_doe", "securePass123")
    with pytest.raises(ValueError) as exc_info:
        create_user("john_doe", "anotherPass")
    assert "Username already exists" in str(exc_info.value)

def test_create_user_unexpected_error(reset_mock_db, monkeypatch):
    def mock_hashpw(*args, **kwargs):
        raise Exception("Hash error")
    monkeypatch.setattr("auth.auth_service.bcrypt.hashpw", mock_hashpw)
    with pytest.raises(Exception) as exc_info:
        create_user("error_user", "errorPass")
    assert "Failed to create user." in str(exc_info.value)

def test_verify_user_success(reset_mock_db):
    created_user = create_user("jane_doe", "MyPassword")
    verified_data = verify_user("jane_doe", "MyPassword")
    assert verified_data["username"] == created_user["username"]
    assert verified_data["id"] == created_user["id"]

def test_verify_user_nonexistent(reset_mock_db):
    with pytest.raises(ValueError) as exc_info:
        verify_user("nonexistent", "pass")
    assert "User does not exist." in str(exc_info.value)

def test_verify_user_wrong_password(reset_mock_db):
    create_user("existing_user", "CorrectPass")
    with pytest.raises(ValueError) as exc_info:
        verify_user("existing_user", "WrongPass")
    assert "Invalid password." in str(exc_info.value)

def test_verify_user_unexpected_error(reset_mock_db, monkeypatch):
    create_user("error_user", "somePass")
    def mock_checkpw(*args, **kwargs):
        raise Exception("Check password error")
    monkeypatch.setattr("auth.auth_service.bcrypt.checkpw", mock_checkpw)
    with pytest.raises(Exception) as exc_info:
        verify_user("error_user", "somePass")
    assert "Failed to verify user." in str(exc_info.value)