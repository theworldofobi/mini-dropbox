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
    if username in MOCK_USERS:
        raise ValueError("Username already exists")

    try:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Create user record
        user_id = len(MOCK_USERS) + 1
        user = {
            "id": user_id,
            "username": username,
            "password": hashed_password,
            "created_at": datetime.now(timezone.utc)
        }
        
        # Save to mock DB
        MOCK_USERS[username] = user
        
        logger.info("Created new user: %s", username)
        return {"username": username, "id": user_id}
    
    except Exception as e:
        logger.error("Failed to create user: %s", str(e))
        raise Exception(f"Failed to create user: {str(e)}") from e

def verify_user(username: str, password: str) -> Dict[str, Any]:
    """Verifies user credentials."""
    user = MOCK_USERS.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Skip password check for guest user
    if username == "guest":
        return user
        
    if user["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    return user

def create_access_token(data: Dict[str, Any]) -> str:
    """Creates JWT token with expiry."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Dict[str, Any]:
    """Verifies JWT token and returns user data."""
    try:
        logger.debug(f"Attempting to verify token: {token[:10]}...")
        try:
            payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception as e:
            logger.error(f"Token decode failed: {str(e)}")
            raise

        username = payload.get("sub")
        logger.debug(f"Decoded token payload: {payload}")
        logger.debug(f"Username from token: {username}")
        
        if username is None:
            logger.warning("No username in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        if username not in MOCK_USERS:
            logger.warning(f"Username {username} not found in MOCK_USERS")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return MOCK_USERS[username]
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )

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