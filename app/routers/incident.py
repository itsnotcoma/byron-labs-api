from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.models.pagination import QueryPaginationParams

from ..models.incident import (
    BodyIncident,
    Incident,
    IncidentDTO,
    IncidentsRes,
    QueryIncidentParams,
)
from ..models.reporter import Reporter
from ..models.sort import QuerySortParams
from ..utils.auth import current_user
from ..utils.incident import (
    INCIDENTS_DB,
    search_incident_by_query,
    search_incident_by_uuid,
)

router = APIRouter(prefix="/incident", tags=["Incident"])


@router.get("/all", response_model=IncidentsRes)
async def get_incidents(
    q: Annotated[QueryIncidentParams, Depends(QueryIncidentParams)],
    pag: Annotated[QueryPaginationParams, Depends(QueryPaginationParams)],
    sort: Annotated[QuerySortParams, Depends(QuerySortParams)],
    auth: Annotated[Reporter, Depends(current_user)],
):
    incidents = search_incident_by_query(q, sort)

    if pag.skip:
        incidents = incidents[pag.skip :]
    if pag.limit:
        incidents = incidents[: pag.limit]

    return {
        "data": incidents,
        "total": len(INCIDENTS_DB),
        "skip": pag.skip or 0,
        "limit": pag.limit or len(INCIDENTS_DB),
    }


@router.get("/{id}")
async def get_incident(id: UUID, auth: Annotated[Reporter, Depends(current_user)]):
    print(id)
    found = search_incident_by_uuid(id)
    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return found


@router.post("/", response_model=IncidentDTO)
async def create_incident(
    incident: Incident, auth: Annotated[Reporter, Depends(current_user)]
):
    resIncident: IncidentsRes = jsonable_encoder(incident)
    resIncident.update(
        {"id": uuid4(), "created_at": datetime.now(), "updated_at": datetime.now()}
    )
    INCIDENTS_DB.append(incident)
    return resIncident


@router.put("/{id}", response_model=IncidentDTO)
async def update_incident(
    id: UUID,
    q: Annotated[BodyIncident, Depends(BodyIncident)],
    auth: Annotated[Reporter, Depends(current_user)],
):
    found = search_incident_by_uuid(id)
    if found is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )

    if q.title is not None:
        found.title = q.title
    if q.description is not None:
        found.description = q.description
    if q.severity is not None:
        found.severity = q.severity
    if q.reporter is not None:
        found.reporter = q.reporter

    return found


@router.delete("/{id}")
async def delete_incident(
    id: UUID,
    auth: Annotated[Reporter, Depends(current_user)],
):
    found = search_incident_by_uuid(id)
    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    INCIDENTS_DB.remove(found)
    return {"message": "Incident deleted successfully"}
