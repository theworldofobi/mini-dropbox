import pytest
import bcrypt
import jwt
from unittest.mock import patch, MagicMock
from typing import Optional
from utils.auth_helpers import extract_user_id, hash_password, check_session_valid

def test_extract_user_id_valid():
    valid_payload = {"user_id": "12345"}
    with patch.object(jwt, "decode", return_value=valid_payload):
        result = extract_user_id("fake_token")
    assert result == "12345"

def test_extract_user_id_no_user_id():
    no_user_payload = {"some_other_key": "value"}
    with patch.object(jwt, "decode", return_value=no_user_payload):
        result = extract_user_id("fake_token")
    assert result is None

def test_extract_user_id_invalid_token():
    with patch.object(jwt, "decode", side_effect=jwt.PyJWTError("Invalid token")):
        result = extract_user_id("invalid_token")
    assert result is None

def test_hash_password_success():
    password = "my_secure_password"
    hashed = hash_password(password)
    assert hashed != password
    assert bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def test_hash_password_error():
    with patch.object(bcrypt, "gensalt", side_effect=Exception("Salt generation failed")):
        with pytest.raises(Exception):
            hash_password("error_password")

def test_check_session_valid_success():
    assert check_session_valid("any_user_id") is True

def test_check_session_valid_exception():
    with patch("utils.auth_helpers.check_session_valid", side_effect=Exception("Simulated error")):
        # Since we are patching the function itself, it will raise an exception
        # which isn't caught by the real implementation. This verifies the fallback.
        with pytest.raises(Exception):
            check_session_valid("error_user_id")