import bcrypt
import jwt as pyjwt
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from config import load_config

logger = logging.getLogger(__name__)

# Load configuration
config = load_config()
SECRET_KEY = config["JWT_SECRET_KEY"]
ALGORITHM = config["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["JWT_EXPIRE_MINUTES"]

# Mock session storage (replace with Redis/database in production)
active_sessions: Dict[str, datetime] = {}

def create_access_token(data: Dict[str, Any]) -> str:
    """Creates a new JWT token with expiration."""
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Created access token for user: %s", data.get("user_id"))
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create access token: %s", str(e))
        raise

def extract_user_id(token: str) -> Optional[str]:
    """Extracts the user ID from a JWT token."""
    try:
        decoded_payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_payload.get("user_id")
        if user_id is not None:
            logger.debug("Extracted user_id from token: %s", user_id)
            return str(user_id)
        logger.warning("No user_id found in token payload")
        return None
    except pyjwt.PyJWTError as e:
        logger.error("Failed to decode token: %s", str(e))
        return None

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    except Exception as e:
        logger.error("Failed to hash password: %s", str(e))
        raise RuntimeError("Password hashing failed") from e

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a password against its hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception as e:
        logger.error("Failed to verify password: %s", str(e))
        return False

def check_session_valid(user_id: str) -> bool:
    """Checks if user's session is valid."""
    try:
        if user_id not in active_sessions:
            return False
            
        session_time = active_sessions[user_id]
        current_time = datetime.utcnow()
        
        # Check if session has expired
        if current_time - session_time > timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
            del active_sessions[user_id]
            logger.info("Session expired for user: %s", user_id)
            return False
            
        # Update session timestamp
        active_sessions[user_id] = current_time
        return True
        
    except Exception as e:
        logger.error("Session validation failed: %s", str(e))
        return False

def create_session(user_id: str) -> None:
    """Creates a new session for a user."""
    try:
        active_sessions[user_id] = datetime.utcnow()
        logger.info("Created new session for user: %s", user_id)
    except Exception as e:
        logger.error("Failed to create session: %s", str(e))
        raise

def invalidate_session(user_id: str) -> None:
    """Invalidates a user's session."""
    try:
        active_sessions.pop(user_id, None)
        logger.info("Invalidated session for user: %s", user_id)
    except Exception as e:
        logger.error("Failed to invalidate session: %s", str(e))
        raise