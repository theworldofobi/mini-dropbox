from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from mini_dropbox.auth.auth_service import get_current_user
from . import share_service

router = APIRouter(prefix="/share", tags=["Sharing"])

# Replace type alias with Pydantic models
class ShareLinkResponse(BaseModel):
    """Response model for share link creation."""
    message: str
    share_url: str
    expires_at: str
    permission_level: str

class ShareAccessResponse(BaseModel):
    """Response model for share access."""
    file_id: str
    permission_level: str
    expires_at: str

class ShareListResponse(BaseModel):
    """Response model for share listing."""
    shares: List[Dict[str, Any]]
    total: int

@router.post("/{file_id}", response_model=ShareLinkResponse)
async def create_share_link_endpoint(
    file_id: str,
    permission: str = share_service.SharePermission.READ,
    expires_in_days: int = 7,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Creates a share link for a file."""
    try:
        share_data = share_service.create_share_link(
            user_id=str(current_user["id"]),
            file_id=file_id,
            permission_level=permission,
            expires_in_days=expires_in_days
        )
        
        return {
            "message": "Share link created successfully",
            "share_url": f"/share/access/{share_data['token']}",
            "expires_at": share_data["expires_at"],
            "permission_level": share_data["permission_level"]
        }
        
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )

@router.get("/access/{token}", response_model=ShareAccessResponse)
async def access_shared_file(token: str) -> Dict[str, Any]:
    """Accesses a shared file using a token."""
    try:
        share_data = share_service.validate_share_token(token)
        
        return {
            "file_id": share_data["file_id"],
            "permission_level": share_data["permission_level"],
            "expires_at": share_data["expires_at"]
        }
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )

@router.delete("/{token}")
async def revoke_share_link_endpoint(
    token: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> ShareLinkResponse:
    """Revokes a share link."""
    try:
        share_service.revoke_share_link(token, str(current_user["id"]))
        return {"message": "Share link revoked successfully"}
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )

@router.get("/list", response_model=ShareListResponse)
async def list_shares_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Lists all active shares for the current user."""
    try:
        shares = share_service.list_user_shares(str(current_user["id"]))
        return {
            "shares": shares,
            "total": len(shares)
        }
        
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )