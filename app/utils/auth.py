from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..core import config
from ..models.reporter import Reporter, ReporterDTO
from ..utils.reporter import search_reporter, search_reporter_db

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def auth_user(
    settings: Annotated[config.Settings, Depends(config.get_settings)],
    token: str = Depends(oauth2),
):
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        ).get("sub")
        print(username)
        if username is None:
            raise unauthorized_exception

    except JWTError:
        raise unauthorized_exception

    return search_reporter_db(username)


async def current_user(reporter: Reporter = Depends(auth_user)):
    if reporter.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return search_reporter(reporter.username)
