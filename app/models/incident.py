from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Body, Query
from pydantic import BaseModel


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Incident(BaseModel):
    title: str
    description: str
    severity: IncidentSeverity
    reporter: str


class IncidentDTO(Incident):
    uuid: UUID
    created_at: datetime
    updated_at: datetime


class IncidentsRes(BaseModel):
    data: list[IncidentDTO]
    total: int
    skip: int
    limit: int


class QueryIncidentParams:
    def __init__(
        self,
        title: Annotated[str, Query()] = None,
        severity: Annotated[IncidentSeverity, Query()] = None,
        reporter: Annotated[str, Query()] = None,
    ):
        self.title = title
        self.severity = severity
        self.reporter = reporter


class BodyIncident:
    def __init__(
        self,
        title: str | None = Body(None),
        description: str | None = Body(None),
        severity: IncidentSeverity | None = Body(None),
        reporter: str | None = Body(None),
    ):
        self.title = title
        self.description = description
        self.severity = severity
        self.reporter = reporter
