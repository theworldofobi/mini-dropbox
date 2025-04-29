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
        print(f"Storing file: {file_obj.filename} for user: {user_id}")
        
        content = await file_obj.read()
        print(f"File size: {len(content)} bytes")

        # Generate unique file ID and path
        file_id = str(uuid.uuid4())
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = UPLOAD_DIR / f"{file_id}{Path(file_obj.filename).suffix}"
        
        # Save file content
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Create metadata
        metadata = {
            "file_id": file_id,
            "original_name": file_obj.filename,
            "size": len(content),
            "user_id": user_id,
            "folder_id": folder_id,
            "created_at": datetime.utcnow(),
            "type": "file",
            "storage_path": str(file_path)  # Add storage path to metadata
        }
        
        # Store in mock database
        _file_db[file_id] = metadata
        print(f"File metadata stored: {metadata}")
        
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
    """Returns a list of file/folder metadata for a given user."""
    try:
        print(f"Listing files for user {user_id}, folder {folder_id}")
        print(f"Current _file_db contents: {_file_db}")
        
        # Filter files by user_id and folder_id
        user_files = [
            metadata for metadata in _file_db.values()
            if metadata["user_id"] == user_id
            and metadata.get("folder_id") == folder_id
        ]

        print(f"Found {len(user_files)} files for user")
        return user_files

    except Exception as e:
        logger.error(f"Failed to list files: {str(e)}")
        raise