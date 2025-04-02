from typing import Any, Dict, List
import logging
from datetime import datetime
from mini_dropbox.files.file_service import _file_db  # Using the mock DB from file_service

logger = logging.getLogger(__name__)

def get_updated_files(user_id: str, last_sync_ts: float) -> List[Dict[str, Any]]:
    """
    Fetches files changed after a timestamp.

    Args:
        user_id: The ID of the user performing the sync.
        last_sync_ts: The last known synchronization timestamp (epoch-based).

    Returns:
        A list of dictionaries containing file metadata for updated files.

    Raises:
        ValueError: If the user ID is invalid or if the provided timestamp is not valid.
    """
    if not user_id:
        raise ValueError("User ID cannot be empty.")

    if last_sync_ts < 0:
        raise ValueError("Timestamp cannot be negative.")

    try:
        # Get all files for the user that were updated after last_sync_ts
        updated_files = [
            file_meta for file_meta in _file_db.values()
            if (file_meta["user_id"] == user_id and 
                file_meta["updated_at"].timestamp() > last_sync_ts)
        ]
        
        logger.info("Found %d updated files for user %s", len(updated_files), user_id)
        return updated_files
        
    except Exception as e:
        logger.error("Failed to get updated files: %s", str(e))
        raise RuntimeError(f"Failed to get updated files: {str(e)}") from e


def detect_conflicts(local_version: Dict[str, Any], remote_version: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determines if a conflict exists between the local and remote file versions,
    and attempts to merge or flag them.

    Args:
        local_version: A dictionary containing metadata of the local file version.
        remote_version: A dictionary containing metadata of the remote file version.

    Returns:
        A dictionary representing the merged version or the result of conflict resolution.

    Raises:
        KeyError: If expected fields are missing from version dictionaries.
    """
    if "version" not in local_version or "version" not in remote_version:
        raise KeyError("Missing 'version' key in version data")

    try:
        local_ver = local_version["version"]
        remote_ver = remote_version["version"]
        local_modified = local_version.get("modified_at", datetime.min)
        remote_modified = remote_version.get("modified_at", datetime.min)

        # If versions match, no conflict
        if local_ver == remote_ver:
            return local_version

        # If versions differ, check timestamps
        if local_modified > remote_modified:
            return {
                **local_version,
                "conflict_status": "resolved_keep_local",
                "conflicting_version": remote_ver
            }
        else:
            return {
                **remote_version,
                "conflict_status": "resolved_keep_remote",
                "conflicting_version": local_ver
            }

    except Exception as e:
        logger.error("Failed to detect conflicts: %s", str(e))
        raise RuntimeError(f"Failed to detect conflicts: {str(e)}") from e