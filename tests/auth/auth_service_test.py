import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Import the functions under test from the project root
from auth.auth_service import create_user, verify_user

@pytest.fixture
def mock_db_session():
    """
    Provides a mock for the SQLAlchemy Session object.
    Setup: Create a MagicMock with Session specification.
    Teardown: Automatically handled by pytest once the test is complete.
    """
    return MagicMock(spec=Session)


@pytest.mark.parametrize("username, password", [
    ("newuser", "newpass"),
    ("anotheruser", "anotherpass")
])
def test_create_user_success(mock_db_session, username, password):
    """
    Test that create_user successfully creates a new user with a hashed password
    and saves it to the database.
    """
    # Mock bcrypt instead of a helper function
    with patch("auth.auth_service.bcrypt.hashpw", return_value=b"mocked_hashed_pwd") as mock_hash:
        with patch("auth.auth_service.bcrypt.gensalt", return_value=b"mock_salt"):
            # Call the function under test
            created_user = create_user(username, password)
        
            # Assert that the hash function was called correctly
            mock_hash.assert_called_once()
            # Check that the first argument to hashpw was the encoded password
            args, _ = mock_hash.call_args
            assert args[0] == password.encode('utf-8')
            
            # Assert the user was created with expected values
            assert created_user["username"] == username
            assert "id" in created_user


def test_create_user_existing_user(mock_db_session):
    """
    Test that create_user raises an exception or handles the scenario
    when attempting to create a user that already exists.
    """
    existing_username = "existinguser"
    existing_password = "somepass"

    # Patch the MOCK_USERS dictionary to include our test user
    with patch("auth.auth_service.MOCK_USERS", {"existinguser": {"username": existing_username}}):
        with pytest.raises(ValueError) as exc_info:
            create_user(existing_username, existing_password)
        assert "already exists" in str(exc_info.value)


def test_verify_user_success(mock_db_session):
    """
    Test that verify_user returns user data when credentials are correct.
    """
    test_username = "validuser"
    test_password = "validpass"
    
    # Create a mock user with the same password (no hashing in the mock)
    mock_user = {
        "username": test_username,
        "password": test_password,  # Use the plain password to match the implementation
        "id": "123"
    }
    
    # Patch MOCK_USERS to include our test user
    with patch("auth.auth_service.MOCK_USERS", {test_username: mock_user}):
        user_data = verify_user(test_username, test_password)
        assert user_data is not None
        assert user_data["username"] == test_username


def test_verify_user_wrong_password(mock_db_session):
    """
    Test that verify_user raises an HTTPException when the password is incorrect.
    """
    test_username = "user1"
    correct_password = "correctpass"
    wrong_password = "wrongpass"
    
    # Create a mock user with the correct password
    mock_user = {
        "username": test_username,
        "password": correct_password,
        "id": "123"
    }
    
    # Patch MOCK_USERS to include our test user
    with patch("auth.auth_service.MOCK_USERS", {test_username: mock_user}):
        # The verify_user function should raise an HTTPException
        with pytest.raises(HTTPException) as exc_info:
            verify_user(test_username, wrong_password)
        # Check that the exception has the expected status code and detail
        assert exc_info.value.status_code == 401
        assert "Invalid password" in str(exc_info.value.detail)


def test_verify_user_nonexistent(mock_db_session):
    """
    Test that verify_user raises an HTTPException when the user doesn't exist.
    """
    test_username = "nonexistent"
    test_password = "nopass"

    # Use an empty MOCK_USERS dictionary to simulate no user found
    with patch("auth.auth_service.MOCK_USERS", {}):
        # The verify_user function should raise an HTTPException
        with pytest.raises(HTTPException) as exc_info:
            verify_user(test_username, test_password)
        # Check that the exception has the expected status code and detail
        assert exc_info.value.status_code == 401
        assert "User not found" in str(exc_info.value.detail)