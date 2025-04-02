from typing import Any, Dict, List, Optional
import os
import uuid
import logging
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile

logger = logging.getLogger(__name__)

# Mock database for file metadata
_file_db: Dict[str, Dict[str, Any]] = {}

# Configuration
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif'}

async def store_file(user_id: str, file_obj: UploadFile, folder_id: str | None = None) -> Dict[str, Any]:
    """Stores a file and returns metadata."""
    try:
        print(f"Storing file: {file_obj.filename} for user: {user_id}")  # Debug print
        
        # Read file content
        content = await file_obj.read()
        print(f"File size: {len(content)} bytes")  # Debug print

        # Here you would normally save the file to storage
        # For now, let's just return metadata
        file_id = f"file_{hash(content)}"
        
        metadata = {
            "file_id": file_id,
            "original_name": file_obj.filename,
            "size": len(content),
            "user_id": user_id,
            "folder_id": folder_id
        }
        
        print(f"File metadata: {metadata}")  # Debug print
        return metadata

    except Exception as e:
        logger.error(f"Failed to store file: {str(e)}")
        raise


def fetch_file(file_id: str) -> Dict[str, Any]:
    """
    Retrieves file bytes and metadata if the user has access.

    Args:
        file_id: The ID of the file to retrieve.

    Returns:
        A dictionary containing the file metadata and bytes.

    Raises:
        ValueError: If the file_id is invalid.
        FileNotFoundError: If the file does not exist or the user has no access.
        RuntimeError: If the fetch operation fails.
    """
    if not file_id:
        raise ValueError("File ID must be provided.")

    try:
        # Get metadata from mock database
        file_metadata = _file_db.get(file_id)
        if not file_metadata:
            raise FileNotFoundError(f"File not found: {file_id}")

        # Read file from disk
        file_path = Path(file_metadata["storage_path"])
        if not file_path.exists():
            raise FileNotFoundError(f"File not found on disk: {file_id}")

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        return {
            "metadata": file_metadata,
            "file_bytes": file_bytes
        }

    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error("Failed to fetch file: %s", str(e))
        raise RuntimeError(f"Failed to fetch file: {str(e)}") from e


def list_user_files(user_id: str, folder_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns a list of file/folder metadata for a given user.

    Args:
        user_id: The ID of the user whose files/folders are to be listed.
        folder_id: The ID of the parent folder for which contents are listed.

    Returns:
        A list of metadata dictionaries, each representing a file or folder.

    Raises:
        ValueError: If the user_id is invalid.
        RuntimeError: If the operation fails.
    """
    if not user_id:
        raise ValueError("User ID must be provided.")

    try:
        # Filter files by user_id and folder_id
        user_files = [
            metadata for metadata in _file_db.values()
            if metadata["user_id"] == user_id
            and metadata["folder_id"] == folder_id
        ]

        # Sort by creation date
        user_files.sort(key=lambda x: x["created_at"], reverse=True)
        
        logger.info("Retrieved %d files for user %s", len(user_files), user_id)
        return user_files

    except Exception as e:
        logger.error("Failed to list files for user %s: %s", user_id, str(e))
        raise RuntimeError(f"Failed to list files: {str(e)}") from e