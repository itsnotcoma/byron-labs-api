from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends

from ..models.incident import (
    IncidentDTO,
    IncidentSeverity,
    IncidentStatus,
    QueryIncidentParams,
)
from ..models.sort import QuerySortParams


def search_incident_by_uuid(id: UUID):
    if id in INCIDENTS_DB:
        return INCIDENTS_DB[id]
    return None


def search_incident_by_query(
    q: Annotated[QueryIncidentParams, Depends(QueryIncidentParams)],
    sort: Annotated[QuerySortParams, Depends(QuerySortParams)],
):
    filtered_incidents = INCIDENTS_DB
    if q.title:
        filtered_incidents = [
            incident
            for incident in INCIDENTS_DB
            if q.title.lower() in incident.title.lower()
        ]

    if q.reporter:
        filtered_incidents = [
            incident
            for incident in filtered_incidents
            if q.reporter.lower() in incident.reporter.lower()
        ]

    if q.severity:
        filtered_incidents = [
            incident
            for incident in filtered_incidents
            if q.severity == incident.severity
        ]

    if q.status:
        filtered_incidents = [
            incident for incident in filtered_incidents if q.status == incident.status
        ]

    valid_sort_by = ["title", "reporter", "severity", "created_at", "updated_at"]
    if sort.sort_by not in valid_sort_by:
        sort.sort_by = "created_at"

    if sort.sort_order not in [-1, 1]:
        sort.sort_order = -1

    reverse = sort.sort_order == -1

    return sorted(
        filtered_incidents,
        key=lambda incident: getattr(incident, sort.sort_by),
        reverse=reverse,
    )


INCIDENTS_DB = [
    IncidentDTO(
        id=uuid4(),
        title="Network Outage",
        description="A network outage has occurred in the main office.",
        severity=IncidentSeverity.HIGH,
        reporter="John Doe",
        created_at=datetime.now() - timedelta(minutes=17),
        updated_at=datetime.now() - timedelta(minutes=17),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Hardware Failure",
        description="Multiple hardware components have malfunctioned.",
        severity=IncidentSeverity.LOW,
        reporter="Michael Brown",
        created_at=datetime.now() - timedelta(minutes=16),
        updated_at=datetime.now() - timedelta(minutes=16),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Data Loss",
        description="Critical data loss due to backup failure.",
        severity=IncidentSeverity.HIGH,
        reporter="Alice Johnson",
        created_at=datetime.now() - timedelta(minutes=15),
        updated_at=datetime.now() - timedelta(minutes=15),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Security Breach",
        description="Unauthorized access to sensitive data.",
        severity=IncidentSeverity.HIGH,
        reporter="Jane Smith",
        created_at=datetime.now() - timedelta(minutes=14),
        updated_at=datetime.now() - timedelta(minutes=14),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Software Bug",
        description="A software bug has caused a system crash.",
        severity=IncidentSeverity.MEDIUM,
        reporter="David White",
        created_at=datetime.now() - timedelta(minutes=13),
        updated_at=datetime.now() - timedelta(minutes=13),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Power Outage",
        description="A power outage has occurred in the building.",
        severity=IncidentSeverity.LOW,
        reporter="Chris Brown",
        created_at=datetime.now() - timedelta(minutes=12),
        updated_at=datetime.now() - timedelta(minutes=12),
    ),
    IncidentDTO(
        id=uuid4(),
        title="System Failure",
        description="A system failure has caused data corruption.",
        severity=IncidentSeverity.HIGH,
        reporter="Sarah Green",
        created_at=datetime.now() - timedelta(minutes=11),
        updated_at=datetime.now() - timedelta(minutes=11),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Server Crash",
        description="A server crash has caused downtime.",
        severity=IncidentSeverity.HIGH,
        reporter="Tom Wilson",
        created_at=datetime.now() - timedelta(minutes=10),
        updated_at=datetime.now() - timedelta(minutes=10),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Database Error",
        description="A database error has caused data inconsistency.",
        severity=IncidentSeverity.MEDIUM,
        reporter="Emily Davis",
        created_at=datetime.now() - timedelta(minutes=9),
        updated_at=datetime.now() - timedelta(minutes=9),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Application Failure",
        description="An application failure has caused data loss.",
        severity=IncidentSeverity.HIGH,
        reporter="Paul Taylor",
        created_at=datetime.now() - timedelta(minutes=8),
        updated_at=datetime.now() - timedelta(minutes=8),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Network Outage",
        description="A network outage has occurred in the main office.",
        severity=IncidentSeverity.HIGH,
        reporter="John Doe",
        created_at=datetime.now() - timedelta(minutes=7),
        updated_at=datetime.now() - timedelta(minutes=7),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Hardware Failure",
        description="Multiple hardware components have malfunctioned.",
        severity=IncidentSeverity.LOW,
        reporter="Michael Brown",
        created_at=datetime.now() - timedelta(minutes=6),
        updated_at=datetime.now() - timedelta(minutes=6),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Data Loss",
        description="Critical data loss due to backup failure.",
        severity=IncidentSeverity.HIGH,
        reporter="Alice Johnson",
        created_at=datetime.now() - timedelta(minutes=5),
        updated_at=datetime.now() - timedelta(minutes=5),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Security Breach",
        description="Unauthorized access to sensitive data.",
        severity=IncidentSeverity.HIGH,
        reporter="Jane Smith",
        created_at=datetime.now() - timedelta(minutes=4),
        updated_at=datetime.now() - timedelta(minutes=4),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Software Bug",
        description="A software bug has caused a system crash.",
        severity=IncidentSeverity.MEDIUM,
        reporter="David White",
        status=IncidentStatus.PAUSED,
        created_at=datetime.now() - timedelta(minutes=3),
        updated_at=datetime.now() - timedelta(minutes=3),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Power Outage",
        description="A power outage has occurred in the building.",
        severity=IncidentSeverity.LOW,
        reporter="Chris Brown",
        status=IncidentStatus.IN_PROGRESS,
        created_at=datetime.now() - timedelta(minutes=2),
        updated_at=datetime.now() - timedelta(minutes=2),
    ),
    IncidentDTO(
        id=uuid4(),
        title="System Failure",
        description="A system failure has caused data corruption.",
        severity=IncidentSeverity.HIGH,
        reporter="Sarah Green",
        created_at=datetime.now() - timedelta(minutes=1),
        updated_at=datetime.now() - timedelta(minutes=1),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Server Crash",
        description="A server crash has caused downtime.",
        severity=IncidentSeverity.HIGH,
        reporter="Tom Wilson",
        status=IncidentStatus.CLOSED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
