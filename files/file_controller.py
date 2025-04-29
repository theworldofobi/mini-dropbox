from typing import Any, Dict, List
import logging
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Form
from fastapi.responses import StreamingResponse
from auth.auth_service import get_current_user
from . import file_service

router = APIRouter(prefix="/files", tags=["Files"])
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_file_endpoint(
    upload_file: UploadFile = File(...),
    folder_id: str | None = Form(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """Handles file upload requests."""
    print("Received file:", upload_file.filename)
    try:
        # Add await here
        file_metadata = await file_service.store_file(
            user_id=str(current_user["id"]),
            file_obj=upload_file,
            folder_id=folder_id
        )
        
        logger.info("File uploaded successfully: %s", file_metadata["file_id"])
        return {
            "message": "File uploaded successfully",
            "file_id": file_metadata["file_id"]
        }

    except Exception as error:
        print("Upload error:", str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )

@router.get("/download/{file_id}")
async def download_file_endpoint(
    file_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> StreamingResponse:
    """Returns file data to the client."""
    try:
        file_data = file_service.fetch_file(file_id)
        
        # Verify user has access to this file
        if str(current_user["id"]) != str(file_data["metadata"]["user_id"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Return file as streaming response
        return StreamingResponse(
            iter([file_data["file_bytes"]]),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={file_data['metadata']['original_name']}"
            }
        )

    except FileNotFoundError:
        logger.warning("File not found: %s", file_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    except Exception as error:
        logger.error("Error downloading file: %s", str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download file"
        )




@router.get("/list")
async def list_files_endpoint(
    current_user: Dict[str, Any] = Depends(get_current_user),
    folder_id: str = None
) -> Dict[str, Any]:
    """Lists files for the authenticated user."""
    print("Getting list of files...")
    print("User:", current_user)
    try:
        files = file_service.list_user_files(
            user_id=str(current_user["id"]),
            folder_id=folder_id
        )
        
        return {
            "files": files,
            "total": len(files)
        }

    except Exception as error:
        logger.error("Error listing files: %s", str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list files"
        )