from typing import Dict, Optional

import secrets

# In-memory store for share tokens (for demonstration purposes only).
# Format:
# {
#     "token_value": {
#         "user_id": str,
#         "file_id": str,
#         "permission_level": str,
#         "is_valid": bool
#     }
# }
share_tokens: Dict[str, Dict[str, str]] = {}


def create_share_link(user_id: str, file_id: str, permission_level: str) -> str:
    """
    Creates a unique share link or token for the given user and file with the specified permission level.

    Args:
        user_id: The ID of the user who is creating the share link.
        file_id: The ID of the file that is being shared.
        permission_level: The level of permission granted to whoever uses this link.

    Returns:
        A newly generated token that can be shared to provide access.
    """
    # TODO: Replace in-memory storage with a robust database solution for production.
    # Generate a secure random token
    token = secrets.token_urlsafe(16)
    share_tokens[token] = {
        "user_id": user_id,
        "file_id": file_id,
        "permission_level": permission_level,
        "is_valid": True
    }
    return token


def validate_share_token(token: str) -> Dict[str, Optional[str]]:
    """
    Checks if a token is valid and returns associated file or an error.

    Args:
        token: The share token to validate.

    Returns:
        A dictionary containing the file_id, user_id, and permission_level if the token is valid,
        or an error message if the token is invalid.

    Raises:
        ValueError: If the token does not exist or is marked invalid.
    """
    # Check if the token exists
    if token not in share_tokens:
        raise ValueError("Share token does not exist.")

    token_data = share_tokens[token]

    # Check if the token is still valid
    if not token_data.get("is_valid"):
        raise ValueError("Share token is invalid.")

    # TODO: Add additional validation checks, such as expiration or revoked status.
    return {
        "file_id": token_data["file_id"],
        "user_id": token_data["user_id"],
        "permission_level": token_data["permission_level"]
    }