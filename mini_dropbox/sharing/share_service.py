from typing import Dict, Optional, List
import logging
import secrets
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Mock database for share tokens
share_tokens: Dict[str, Dict[str, any]] = {}

class SharePermission:
    READ = "read"
    WRITE = "write"
    NONE = "none"

def create_share_link(user_id: str, file_id: str, permission_level: str = SharePermission.READ, 
                     expires_in_days: int = 7) -> Dict[str, any]:
    """Creates a unique share link with expiration."""
    try:
        # Generate a secure random token
        token = secrets.token_urlsafe(32)
        
        # Set expiration date
        expiration_date = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Create share record
        share_data = {
            "token": token,
            "user_id": user_id,
            "file_id": file_id,
            "permission_level": permission_level,
            "is_valid": True,
            "created_at": datetime.utcnow(),
            "expires_at": expiration_date,
            "access_count": 0
        }
        
        share_tokens[token] = share_data
        logger.info("Created share link for file %s by user %s", file_id, user_id)
        
        return share_data
        
    except Exception as e:
        logger.error("Failed to create share link: %s", str(e))
        raise RuntimeError(f"Failed to create share link: {str(e)}") from e

def validate_share_token(token: str) -> Dict[str, any]:
    """Validates token and returns associated file data."""
    try:
        # Check if token exists
        if token not in share_tokens:
            raise ValueError("Share token does not exist")

        share_data = share_tokens[token]
        
        # Check validity
        if not share_data["is_valid"]:
            raise ValueError("Share token has been revoked")
            
        # Check expiration
        if datetime.utcnow() > share_data["expires_at"]:
            share_data["is_valid"] = False
            raise ValueError("Share token has expired")
            
        # Update access count
        share_data["access_count"] += 1
        
        logger.info("Validated share token for file %s", share_data["file_id"])
        return share_data
        
    except ValueError:
        raise
    except Exception as e:
        logger.error("Error validating share token: %s", str(e))
        raise RuntimeError(f"Failed to validate share token: {str(e)}") from e

def revoke_share_link(token: str, user_id: str) -> None:
    """Revokes a share link."""
    try:
        if token not in share_tokens:
            raise ValueError("Share token does not exist")
            
        share_data = share_tokens[token]
        
        # Verify ownership
        if share_data["user_id"] != user_id:
            raise ValueError("Unauthorized to revoke this share link")
            
        share_data["is_valid"] = False
        logger.info("Revoked share token for file %s", share_data["file_id"])
        
    except ValueError:
        raise
    except Exception as e:
        logger.error("Failed to revoke share token: %s", str(e))
        raise RuntimeError(f"Failed to revoke share token: {str(e)}") from e

def list_user_shares(user_id: str) -> List[Dict[str, any]]:
    """Lists all active shares for a user."""
    try:
        user_shares = [
            share for share in share_tokens.values()
            if share["user_id"] == user_id and share["is_valid"]
        ]
        
        # Sort by creation date
        user_shares.sort(key=lambda x: x["created_at"], reverse=True)
        return user_shares
        
    except Exception as e:
        logger.error("Failed to list shares for user %s: %s", user_id, str(e))
        raise RuntimeError(f"Failed to list shares: {str(e)}") from e