from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from .auth_service import (
    create_user, 
    verify_user, 
    create_access_token, 
    get_current_user,
    MOCK_USERS
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class UserCredentials(BaseModel):
    """
    Model for user login credentials.
    """
    username: str
    password: str


class Token(BaseModel):
    """Model for access token response."""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup_endpoint(credentials: UserCredentials) -> Dict[str, str]:
    """
    Creates a new user with a username and password.

    Args:
        credentials (UserCredentials): Contains the username and password for the new user.

    Returns:
        Dict[str, str]: A dictionary with a success message or error details.
    """
    try:
        user = create_user(credentials.username, credentials.password)
        return {"message": "User created successfully", "user_id": user["id"]}
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        ) from error


@router.post("/login")
async def login(request: LoginRequest) -> Dict[str, Any]:
    """Login endpoint that returns JWT token."""
    try:
        user = verify_user(request.username, request.password)
        token = create_access_token({"sub": user["username"]})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/guest-login")
async def guest_login() -> Dict[str, Any]:
    """Creates guest token."""
    try:
        # Get guest user from mock database
        user = MOCK_USERS["guest"]
        token = create_access_token({"sub": "guest"})
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/logout")
def logout_endpoint(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Invalidates the user's token.

    Returns:
        Dict[str, str]: Confirmation message upon successful logout.
    """
    try:
        # Get current user to verify token is valid
        current_user = get_current_user(token)
        # In a real implementation, you might want to blacklist the token
        # or implement a proper token revocation mechanism
        return {"message": f"User {current_user['username']} successfully logged out"}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed"
        ) from error


# Dependency for protected routes
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    return get_current_user(token)