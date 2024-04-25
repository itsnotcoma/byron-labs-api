from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.pagination import QueryPaginationParams

from ..models.reporter import Reporter, ReportersRes
from ..utils.auth import current_user
from ..utils.reporter import REPORTERS_DB

router = APIRouter(prefix="/reporter", tags=["Reporter"])


@router.get("/all", response_model=ReportersRes)
async def get_reporters_all(
    pag: Annotated[QueryPaginationParams, Depends(QueryPaginationParams)],
    auth: Annotated[Reporter, Depends(current_user)],
):
    reporters = list(REPORTERS_DB.values())
    if pag.skip:
        reporters = reporters[pag.skip :]
    if pag.limit:
        reporters = reporters[: pag.limit]

    return {
        "data": reporters,
        "total": len(REPORTERS_DB),
        "skip": pag.skip or 0,
        "limit": pag.limit or len(REPORTERS_DB),
    }
