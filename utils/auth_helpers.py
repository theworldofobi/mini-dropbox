import bcrypt
import jwt
from typing import Optional

SECRET_KEY: str = "CHANGE_ME_IN_PROD"  # TODO: Replace with your securely stored secret key
ALGORITHM: str = "HS256"  # TODO: Replace with appropriate JWT algorithm if needed


def extract_user_id(token: str) -> Optional[str]:
    """
    Extracts the user ID from a given JWT token.

    Args:
        token: The JWT token containing user information.

    Returns:
        The user ID as a string if present and valid, otherwise None.
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_payload.get("user_id")
        if user_id is not None:
            return str(user_id)
        return None
    except jwt.PyJWTError:
        # TODO: Log error details
        return None


def hash_password(password: str) -> str:
    """
    Hashes a password using a salted hash approach.

    Args:
        password: The plain-text password.

    Returns:
        A salted hash of the password as a string.
    """
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    except Exception:
        # TODO: Log error details
        # Re-raise or handle the exception appropriately
        raise


def check_session_valid(user_id: str) -> bool:
    """
    Checks if the user's session is still valid.

    Args:
        user_id: The user's unique identifier.

    Returns:
        True if the session is valid, False otherwise.
    """
    try:
        # TODO: Implement session validation logic
        return True
    except Exception:
        # TODO: Log error details
        return False