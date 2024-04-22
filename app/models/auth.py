from uuid import UUID

from pydantic import BaseModel


class AuthRes(BaseModel):
    id: UUID
    username: str
    name: str
    email: str
    company: str
    access_token: str
