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
):
    found = search_incident_by_query(q)
    incidents = found[pag.skip : pag.skip + pag.limit]
    return {
        "data": incidents,
        "total": len(INCIDENTS_DB),
        "skip": pag.skip,
        "limit": pag.limit,
    }


@router.get("/{uuid}")
async def get_incident(id: UUID):
    found = search_incident_by_uuid(uuid)
    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    return found


@router.post("/", response_model=IncidentDTO)
async def create_incident(incident: Incident):
    resIncident: IncidentsRes = jsonable_encoder(incident)
    resIncident.update(
        {"id": uuid4(), "created_at": datetime.now(), "updated_at": datetime.now()}
    )
    print(datetime.now())
    INCIDENTS_DB.append(incident)
    return resIncident


@router.put("/{incident_id}", response_model=IncidentDTO)
async def update_incident(
    incident_id: UUID,
    q: Annotated[BodyIncident, Depends(BodyIncident)],
):
    found = search_incident_by_uuid(incident_id)
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


@router.delete("/{uuid}")
async def delete_incident(id: UUID):
    found = search_incident_by_uuid(uuid)
    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )
    INCIDENTS_DB.remove(found)
    return {"message": "Incident deleted successfully"}
