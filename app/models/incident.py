from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from fastapi import Body, Query
from pydantic import BaseModel

from ..models.reporter import Reporter


class IncidentSeverity(str, Enum):
    """
    Enum representing the severity levels of an incident.
    """

    LOW = "low"  # Low severity
    MEDIUM = "medium"  # Medium severity
    HIGH = "high"  # High severity


class IncidentStatus(str, Enum):
    """
    Enum representing the status of an incident.
    """

    NOT_STARTED = "not_started"  # Incident hasn't started
    IN_PROGRESS = "in_progress"  # Incident is in progress
    PAUSED = "paused"  # Incident is paused
    CLOSED = "closed"  # Incident is closed or resolved


class Incident(BaseModel):
    """
    Base model representing an incident.

    This class encapsulates the common attributes of an incident,
    such as title, description, severity, reporter, status, and date.
    """

    title: str  # Title of the incident
    description: str  # Description of the incident
    severity: IncidentSeverity  # Severity level of the incident
    reporter: Reporter  # Person or entity reporting the incident
    status: IncidentStatus = (
        IncidentStatus.NOT_STARTED
    )  # Current status of the incident
    date: datetime  # Date when the incident occurred


class IncidentDTO(Incident):
    """
    Extended incident model for Data Transfer Object (DTO) purposes.

    This class extends the base Incident model with additional attributes
    such as id, created_at, and updated_at, to track unique identifiers and
    timestamps.
    """

    id: UUID  # Unique identifier for the incident
    created_at: datetime = datetime.now()  # Timestamp for when the incident was created
    updated_at: datetime = (
        datetime.now()
    )  # Timestamp for when the incident was last updated


class IncidentsRes(BaseModel):
    """
    Response model for returning a list of incidents.

    This class contains a list of IncidentDTO objects, along with metadata
    about the total count of incidents, the number of skipped records, and the limit on the returned data.
    """

    data: list[IncidentDTO]  # List of incident data transfer objects
    total: int  # Total number of incidents
    skip: int  # Number of records skipped (for pagination)
    limit: int  # Limit on the number of records returned


class IncidentQueryParams:
    """
    Query parameters for filtering incidents.

    This class is used to define the expected query parameters for incident-related endpoints,
    allowing filtering based on various attributes such as title, severity, reporter, and status.
    """

    def __init__(
        self,
        title: Annotated[str, Query()] = None,  # Filter by incident title
        severity: Annotated[IncidentSeverity, Query()] = None,  # Filter by severity
        reporter: Annotated[str, Query()] = None,  # Filter by reporter
        status: Annotated[IncidentStatus, Query()] = None,  # Filter by status
    ):
        self.title = title  # Incident title
        self.severity = severity  # Severity of the incident
        self.reporter = reporter  # Reporter of the incident
        self.status = status  # Current status of the incident


class IncidentBody:
    """
    Expected body parameters for creating or updating incidents.

    This class defines the attributes expected in the request body for
    incident-related endpoints, allowing you to create or update incidents.
    """

    def __init__(
        self,
        title: str | None = Body(None),  # Title of the incident
        description: str | None = Body(None),  # Description of the incident
        severity: IncidentSeverity | None = Body(
            None
        ),  # Severity level of the incident
        reporter: Reporter | None = Body(None),  # Reporter of the incident
        status: IncidentStatus | None = Body(None),  # Current status of the incident
        date: datetime | None = Body(None),  # Date of the incident
    ):
        self.title = title  # Incident title
        self.description = description  # Incident description
        self.severity = severity  # Severity of the incident
        self.reporter = reporter  # Reporter of the incident
        self.status = status  # Current status of the incident
        self.date = date  # Incident date
