from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.reporter import Reporter
from ..utils.auth import current_user
from ..utils.reporter import REPORTERS_DB, search_reporter_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    found = REPORTERS_DB.get(form_data.username)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    user = search_reporter_db(form_data.username)
    if not form_data.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return {"access_token": form_data.username, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(reporter: Reporter = Depends(current_user)):
    return reporter
