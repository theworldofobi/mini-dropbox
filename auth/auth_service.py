from typing import Any, Dict
import bcrypt

# TODO: Replace with real database interactions
# For demonstration only, this will act as an in-memory store
_mock_db: Dict[str, Dict[str, Any]] = {}


def create_user(username: str, password: str) -> Dict[str, Any]:
    """
    Inserts a new user record with a hashed password.

    Args:
        username: The desired username.
        password: The raw password to be hashed and stored.

    Returns:
        A dictionary containing user information.

    Raises:
        ValueError: If the username already exists.
        Exception: If an unexpected error occurs.
    """
    if username in _mock_db:
        raise ValueError("Username already exists.")

    try:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Save user to mock DB
        _mock_db[username] = {
            "username": username,
            "password": hashed_password,
            "id": len(_mock_db)  # TODO: Replace with real ID from database
        }
        return {"username": username, "id": _mock_db[username]["id"]}
    except Exception as e:
        # TODO: Add proper logging
        raise Exception("Failed to create user.") from e


def verify_user(username: str, password: str) -> Dict[str, Any]:
    """
    Checks the provided credentials against the database and returns user data if correct.

    Args:
        username: The username to verify.
        password: The raw password to check.

    Returns:
        A dictionary containing user information if the credentials are correct.

    Raises:
        ValueError: If the username does not exist or the password is incorrect.
        Exception: If an unexpected error occurs.
    """
    if username not in _mock_db:
        raise ValueError("User does not exist.")

    try:
        stored_user = _mock_db[username]
        stored_hashed_password = stored_user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            return {"username": stored_user["username"], "id": stored_user["id"]}
        else:
            raise ValueError("Invalid password.")
    except Exception as e:
        # TODO: Add proper logging
        raise Exception("Failed to verify user.") from e