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
from ..utils.reporter import REPORTERS_DB, search_reporter, search_reporter_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
async def read_users_me(reporter: Reporter = Depends(current_user)):
    return reporter


@router.post("/login", response_model=AuthRes)
async def login(
    settings: Annotated[config.Settings, Depends(config.get_settings)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    found = REPORTERS_DB.get(form_data.username)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    reporter = search_reporter_db(form_data.username)

    if not reporter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    if not crypt.verify(form_data.password, reporter.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    if reporter.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    payload = {
        "sub": reporter.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiration),
    }

    access_token = jwt.encode(
        payload, settings.jwt_secret, algorithm=settings.jwt_algorithm
    )

    return {
        "id": reporter.id,
        "username": reporter.username,
        "name": reporter.name,
        "email": reporter.email,
        "company": reporter.company,
        "access_token": access_token,
    }
