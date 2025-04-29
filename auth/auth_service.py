from typing import Any, Dict, Optional
from datetime import datetime, timedelta, timezone
import logging
import bcrypt
import jwt as pyjwt

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = "your-secure-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock user database
MOCK_USERS = {
    "suhaas": {
        "id": "1",
        "username": "suhaas",
        "password": "123"  # In production, use hashed passwords
    },
    "guest": {
        "id": "2",
        "username": "guest",
        "password": None
    }
}

def create_user(username: str, password: str) -> Dict[str, Any]:
    """Creates a new user with hashed password."""
    # TODO: Implement user creation functionality
    # 1. Check if username already exists in MOCK_USERS, raise ValueError if it does
    # 2. Hash the password using bcrypt
    # 3. Create a user record with id, username, hashed password, and creation timestamp
    # 4. Add the user to MOCK_USERS dictionary
    # 5. Log successful user creation
    # 6. Return user info (username and id)
    # 7. Handle exceptions appropriately
    pass

def verify_user(username: str, password: str) -> Dict[str, Any]:
    """Verifies user credentials."""
    # TODO: Implement user verification functionality
    # 1. Check if username exists in MOCK_USERS, raise 401 if not found
    # 2. For guest user, skip password check
    # 3. For regular users, verify password matches
    # 4. Return user data if credentials are valid
    # 5. Raise 401 UNAUTHORIZED for invalid credentials
    pass

def create_access_token(data: Dict[str, Any]) -> str:
    """Creates JWT token with expiry."""
    # TODO: Implement token creation
    # 1. Create a copy of the data dictionary
    # 2. Calculate expiration time using ACCESS_TOKEN_EXPIRE_MINUTES
    # 3. Add expiration to token data
    # 4. Encode and return JWT token using SECRET_KEY and ALGORITHM
    pass

def verify_token(token: str) -> Dict[str, Any]:
    """Verifies JWT token and returns user data."""
    # TODO: Implement token verification
    # 1. Try to decode the token using SECRET_KEY and ALGORITHM
    # 2. Extract username ("sub") from payload
    # 3. Validate that username exists and is in MOCK_USERS
    # 4. Return user data if token is valid
    # 5. Handle exceptions with appropriate HTTP errors
    pass

# def get_current_user(token: str) -> Dict[str, Any]:
#     """Dependency for protected endpoints."""
#     print("Checking auth token:", token[:10] if token else None)  # Debug print
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )
#     return verify_token(token.replace("Bearer ", ""))

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    return verify_token(token)