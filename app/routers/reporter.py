from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.pagination import QueryPaginationParams
from app.models.reporter import QueryReporterParams, ReportersRes
from app.utils.reporter import REPORTERS_DB, search_reporters_by_query

router = APIRouter(prefix="/reporter", tags=["Reporter"])


@router.get("/all", response_model=ReportersRes)
async def get_reporters_all(
    pag: Annotated[QueryPaginationParams, Depends(QueryPaginationParams)],
):
    items = list(REPORTERS_DB.values())[pag.skip : pag.skip + pag.limit]
    return {
        "data": items,
        "total": len(REPORTERS_DB),
        "skip": pag.skip,
        "limit": pag.limit,
    }
