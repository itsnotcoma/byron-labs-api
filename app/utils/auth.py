from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..utils.reporter import search_reporter

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


async def current_user(token: str = Depends(oauth2)):
    user = search_reporter(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user
