import json
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from ..core import config
from ..models.auth import AuthRes
from ..models.reporter import Reporter
from ..utils.auth import crypt, current_user
from ..utils.reporter import REPORTERS_DB, search_reporter_db

# Create a FastAPI router with a prefix for authentication endpoints
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def read_users_me(auth: Reporter = Depends(current_user)):
    """
    Endpoint to get information about the currently authenticated user.

    This endpoint uses dependency injection to get the current authenticated
    reporter (user) and returns their information.
    """
    return auth  # Return the authenticated user's information


@router.post("/login", response_model=AuthRes)
async def login(
    settings: Annotated[
        config.Settings, Depends(config.get_settings)
    ],  # Inject configuration settings
    form_data: Annotated[
        OAuth2PasswordRequestForm, Depends()
    ],  # Form data for login (username and password)
):
    """
    Endpoint to authenticate a user and generate an access token.

    This endpoint receives login form data and validates the provided username
    and password. If valid, it generates a JWT access token with user information.
    """

    # Check if the username exists in the database
    found = REPORTERS_DB.get(form_data.username)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    # Retrieve the reporter's information from the database
    reporter = search_reporter_db(form_data.username)

    if not reporter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    # Verify the provided password with the stored encrypted password
    if not crypt.verify(form_data.password, reporter.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    # Check if the reporter's account is disabled
    if reporter.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create a JWT payload with a subject and expiration time
    payload = {
        "sub": reporter.username,  # Subject of the JWT (username)
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.jwt_expiration),  # Token expiration time
    }

    # Encode the JWT with the provided secret and algorithm
    access_token = jwt.encode(
        payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )

    # Return user information and the generated access token
    return {
        "id": reporter.id,
        "username": reporter.username,
        "name": reporter.name,
        "email": reporter.email,
        "company": reporter.company,
        "access_token": access_token,  # JWT access token for authentication
    }
