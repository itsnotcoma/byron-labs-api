from uuid import UUID

from pydantic import BaseModel


class AuthRes(BaseModel):
    """
    Represents the response returned after successful authentication or login.

    This class contains information about the authenticated user, along with
    the generated access token used for subsequent authorized requests.
    """

    id: UUID  # Unique identifier for the user
    username: str  # The user's chosen username
    name: str  # The user's full name
    email: str  # The user's email address
    company: str  # The company with which the user is affiliated
    access_token: str  # JWT access token for authorization
