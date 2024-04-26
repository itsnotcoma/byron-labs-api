from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.models.pagination import PaginationQueryParams

from ..models.incident import (
    Incident,
    IncidentBody,
    IncidentDTO,
    IncidentQueryParams,
    IncidentsRes,
)
from ..models.reporter import Reporter
from ..models.sort import SortQueryParams
from ..utils.auth import current_user
from ..utils.incident import (
    INCIDENTS_DB,
    search_incident_by_query,
    search_incident_by_uuid,
)

# Create a FastAPI router with a prefix for incident endpoints
router = APIRouter(prefix="/incident", tags=["Incident"])


@router.get("/all", response_model=IncidentsRes)
async def get_incidents(
    q: Annotated[
        IncidentQueryParams, Depends(IncidentQueryParams)
    ],  # Query parameters for incidents
    pag: Annotated[
        PaginationQueryParams, Depends(PaginationQueryParams)
    ],  # Pagination parameters
    sort: Annotated[SortQueryParams, Depends(SortQueryParams)],  # Sorting parameters
    auth: Annotated[Reporter, Depends(current_user)],  # Current authenticated user
):
    """
    Retrieve a list of incidents with optional query, pagination, and sorting parameters.

    This endpoint returns all incidents, with optional filtering, pagination, and sorting.
    The response includes metadata for pagination, such as total count, skipped records,
    and limit on the returned data.
    """
    incidents = search_incident_by_query(
        q, sort
    )  # Retrieve incidents based on query parameters

    # Apply pagination
    if pag.skip:
        incidents = incidents[pag.skip :]
    if pag.limit:
        incidents = incidents[: pag.limit]

    return {
        "data": incidents,  # List of incidents
        "total": len(INCIDENTS_DB),  # Total number of incidents
        "skip": pag.skip or 0,  # Number of skipped records
        "limit": pag.limit or len(INCIDENTS_DB),  # Limit on the returned data
    }


@router.get("/{id}")
async def get_incident(id: UUID, auth: Annotated[Reporter, Depends(current_user)]):
    """
    Retrieve a specific incident by its unique identifier.

    This endpoint returns an incident based on the provided UUID. If the incident is not found,
    it raises an HTTP 404 exception.
    """
    found = search_incident_by_uuid(id)  # Find the incident by its UUID
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return found  # Return the found incident


@router.post("/", response_model=IncidentDTO)
async def create_incident(
    body: Annotated[IncidentBody, Depends(IncidentBody)],
    auth: Annotated[Reporter, Depends(current_user)],
):
    """
    Create a new incident.

    This endpoint allows you to create a new incident. It takes an `Incident` object as input
    and generates additional data, such as a unique identifier and timestamps, before adding
    it to the database.
    """

    # Create a new incident with the provided data
    new_incident = IncidentDTO(
        id=uuid4(),  # Generate a new UUID for the incident
        created_at=datetime.now(),  # Set the creation timestamp
        updated_at=datetime.now(),  # Set the update timestamp
        **jsonable_encoder(body)  # Convert the body to a dictionary
    )

    INCIDENTS_DB.append(new_incident)  # Add the new incident to the database

    return new_incident  # Return the created incident with additional data


@router.put("/{id}", response_model=IncidentDTO)
async def update_incident(
    id: UUID,
    body: Annotated[IncidentBody, Depends(IncidentBody)],  # Data to update the incident
    auth: Annotated[Reporter, Depends(current_user)],  # Current authenticated user
):
    """
    Update an existing incident.

    This endpoint allows you to update an incident with new data. If the incident with the given
    UUID doesn't exist, it raises an HTTP 404 exception.
    """
    found = search_incident_by_uuid(id)  # Find the incident by its UUID
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )

    # Update the incident with new data if provided
    if body.title is not None:
        found.title = body.title
    if body.description is not None:
        found.description = body.description
    if body.severity is not None:
        found.severity = body.severity
    if body.reporter is not None:
        found.reporter = body.reporter
    if body.status is not None:
        found.status = body.status
    if body.date is not None:
        found.date = body.date
    found.updated_at = datetime.now()  # Update the timestamp

    return found  # Return the updated incident


@router.delete("/{id}")
async def delete_incident(
    id: UUID,
    auth: Annotated[Reporter, Depends(current_user)],  # Current authenticated user
):
    """
    Delete an incident by its unique identifier.

    This endpoint deletes an incident with the given UUID. If the incident doesn't exist,
    it raises an HTTP 404 exception.
    """
    found = search_incident_by_uuid(id)  # Find the incident by its UUID
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    INCIDENTS_DB.remove(found)  # Remove the found incident from the database
    return {"message": "Incident deleted successfully"}  # Return success message
