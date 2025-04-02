from typing import Any, Dict
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from mini_dropbox.auth.auth_service import get_current_user
from . import sync_service
from datetime import datetime

router = APIRouter(prefix="/sync", tags=["Sync"])
logger = logging.getLogger(__name__)

@router.post("/init")
async def init_sync_endpoint(
    last_sync_ts: float,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Initializes sync and returns changed files."""
    try:
        changed_files = sync_service.get_updated_files(
            user_id=str(current_user["id"]),
            last_sync_ts=last_sync_ts
        )
        
        return {
            "changed_files": changed_files,
            "current_timestamp": datetime.utcnow().timestamp()
        }
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error("Sync initialization failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize sync"
        )

@router.post("/resolve")
async def resolve_conflict_endpoint(
    local_version: Dict[str, Any],
    remote_version: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Resolves conflicts between file versions."""
    try:
        resolution = sync_service.detect_conflicts(local_version, remote_version)
        
        return {
            "resolved_version": resolution,
            "timestamp": datetime.utcnow().timestamp()
        }
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error("Conflict resolution failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resolve conflict"
        )