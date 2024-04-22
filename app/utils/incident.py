from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends

from ..models.incident import IncidentDTO, IncidentSeverity, QueryIncidentParams


def search_incident_by_uuid(id: UUID):
    if uuid in INCIDENTS_DB:
        return INCIDENTS_DB[uuid]
    return None


def search_incident_by_query(
    q: Annotated[QueryIncidentParams, Depends(QueryIncidentParams)]
):
    filtered_incidents = INCIDENTS_DB
    if q.title:
        filtered_incidents = [
            incident
            for incident in INCIDENTS_DB
            if q.title.lower() in incident.title.lower()
        ]

    if q.description:
        filtered_incidents = [
            incident
            for incident in filtered_incidents
            if q.description.lower() in incident.description.lower()
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

    return filtered_incidents


INCIDENTS_DB = [
    IncidentDTO(
        id=uuid4(),
        title="Network Outage",
        description="A network outage has occurred in the main office.",
        severity=IncidentSeverity.HIGH,
        reporter="John Doe",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Hardware Failure",
        description="Multiple hardware components have malfunctioned.",
        severity=IncidentSeverity.LOW,
        reporter="Michael Brown",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Data Loss",
        description="Critical data loss due to backup failure.",
        severity=IncidentSeverity.HIGH,
        reporter="Alice Johnson",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Security Breach",
        description="Unauthorized access to sensitive data.",
        severity=IncidentSeverity.HIGH,
        reporter="Jane Smith",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Software Bug",
        description="A software bug has caused a system crash.",
        severity=IncidentSeverity.MEDIUM,
        reporter="David White",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Power Outage",
        description="A power outage has occurred in the building.",
        severity=IncidentSeverity.LOW,
        reporter="Chris Brown",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="System Failure",
        description="A system failure has caused data corruption.",
        severity=IncidentSeverity.HIGH,
        reporter="Sarah Green",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Server Crash",
        description="A server crash has caused downtime.",
        severity=IncidentSeverity.HIGH,
        reporter="Tom Wilson",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Database Error",
        description="A database error has caused data inconsistency.",
        severity=IncidentSeverity.MEDIUM,
        reporter="Emily Davis",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Application Failure",
        description="An application failure has caused data loss.",
        severity=IncidentSeverity.HIGH,
        reporter="Paul Taylor",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Network Outage",
        description="A network outage has occurred in the main office.",
        severity=IncidentSeverity.HIGH,
        reporter="John Doe",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Hardware Failure",
        description="Multiple hardware components have malfunctioned.",
        severity=IncidentSeverity.LOW,
        reporter="Michael Brown",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Data Loss",
        description="Critical data loss due to backup failure.",
        severity=IncidentSeverity.HIGH,
        reporter="Alice Johnson",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Security Breach",
        description="Unauthorized access to sensitive data.",
        severity=IncidentSeverity.HIGH,
        reporter="Jane Smith",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Software Bug",
        description="A software bug has caused a system crash.",
        severity=IncidentSeverity.MEDIUM,
        reporter="David White",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Power Outage",
        description="A power outage has occurred in the building.",
        severity=IncidentSeverity.LOW,
        reporter="Chris Brown",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="System Failure",
        description="A system failure has caused data corruption.",
        severity=IncidentSeverity.HIGH,
        reporter="Sarah Green",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
    IncidentDTO(
        id=uuid4(),
        title="Server Crash",
        description="A server crash has caused downtime.",
        severity=IncidentSeverity.HIGH,
        reporter="Tom Wilson",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    ),
]
