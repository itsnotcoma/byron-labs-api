from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class Reporter(BaseModel):
    username: str
    name: str
    email: str
    company: str


class ReporterDTO(Reporter):
    id: UUID
    password: str
    disabled: bool
    created_at: datetime
    updated_at: datetime


class ReportersRes(BaseModel):
    data: list[ReporterDTO]
    total: int
    skip: int
    limit: int


class QueryReporterParams:
    def __init__(
        self,
        first_name: Annotated[str, Query()] = None,
        last_name: Annotated[str, Query()] = None,
        username: Annotated[str, Query()] = None,
        company: Annotated[str, Query()] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.company = company
