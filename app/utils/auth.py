from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from ..core import config
from ..models.reporter import Reporter
from ..utils.reporter import search_reporter, search_reporter_db

# OAuth2PasswordBearer is used to obtain the OAuth2 token from request headers.
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# CryptContext with bcrypt for password hashing and verification.
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def auth_user(
    settings: Annotated[config.Settings, Depends(config.get_settings)],
    token: str = Depends(oauth2),
):
    """
    Authenticate a user using an OAuth2 token and JWT.

    This function decodes the OAuth2 token to retrieve the username
    from the JWT payload. If the token is invalid or expired, it raises
    an HTTP 401 exception.
    """
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

        if username is None:
            raise unauthorized_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    except JWTError:
        raise unauthorized_exception

    return search_reporter_db(username)


async def current_user(reporter: Reporter = Depends(auth_user)):
    """
    Retrieve the current authenticated user.

    This function gets the current user from the `auth_user` dependency.
    If the user is disabled, it raises an HTTP 400 exception.
    """
    if reporter.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return search_reporter(reporter.username)
