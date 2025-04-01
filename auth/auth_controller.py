from typing import Dict
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserCredentials(BaseModel):
    """
    Model for user login credentials.
    """
    username: str
    password: str


@router.post("/signup")
def signup_endpoint(credentials: UserCredentials) -> Dict[str, str]:
    """
    Creates a new user with a username and password.

    Args:
        credentials (UserCredentials): Contains the username and password for the new user.

    Returns:
        Dict[str, str]: A dictionary with a success message or error details.
    """
    # TODO: Implement user creation logic
    try:
        # TODO: Save user to database
        return {"message": "User created successfully"}
    except Exception as error:
        # TODO: Replace with more specific error handling
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while creating the user"
        ) from error


@router.post("/login")
def login_endpoint(credentials: UserCredentials) -> Dict[str, str]:
    """
    Authenticates a user and returns a session or JWT.

    Args:
        credentials (UserCredentials): Contains the username and password for the user.

    Returns:
        Dict[str, str]: A dictionary with the session token or JWT.
    """
    # TODO: Implement user authentication logic
    try:
        # TODO: Verify user's credentials and generate token
        return {"token": "fake-jwt-token"}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        ) from error


@router.post("/logout")
def logout_endpoint() -> Dict[str, str]:
    """
    Invalidates the user's session or token.

    Returns:
        Dict[str, str]: Confirmation message upon successful logout.
    """
    # TODO: Implement logout logic
    try:
        # TODO: Invalidate token or session
        return {"message": "Successfully logged out"}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while logging out"
        ) from error