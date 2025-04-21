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
    # TODO: Implement user signup functionality
    # 1. Call create_user with the provided username and password
    # 2. Return success message with user_id and username
    # 3. Handle ValueError for when user already exists (409 CONFLICT)
    # 4. Handle other exceptions with 500 INTERNAL_SERVER_ERROR
    pass


@router.post("/login")
async def login(request: LoginRequest) -> Dict[str, Any]:
    """Login endpoint that returns JWT token."""
    # TODO: Implement user login functionality
    # 1. Verify user credentials using verify_user function
    # 2. Check if verification returns None - if so, raise 401 UNAUTHORIZED
    # 3. Create an access token with the user's username
    # 4. Return token in proper format with bearer type
    # 5. Handle exceptions and return appropriate error responses
    pass


@router.post("/guest-login")
async def guest_login() -> Dict[str, Any]:
    """Creates guest token."""
    # TODO: Implement guest login functionality
    # 1. Get the guest user from MOCK_USERS
    # 2. Create an access token for "guest" user
    # 3. Return token with bearer type
    # 4. Handle exceptions with 500 INTERNAL_SERVER_ERROR
    pass


@router.post("/logout")
def logout_endpoint(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Invalidates the user's token.

    Returns:
        Dict[str, str]: Confirmation message upon successful logout.
    """
    # TODO: Implement logout functionality
    # 1. Handle test case where token is "valid_token_for_user"
    # 2. Get current user to verify token is valid
    # 3. Return successful logout message with username
    # 4. Handle exceptions with 401 UNAUTHORIZED
    pass


# Dependency for protected routes
def get_current_user_dependency(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    # This is a regular function that calls the imported get_current_user
    return get_current_user(token)