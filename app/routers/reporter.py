from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.pagination import PaginationQueryParams

from ..models.reporter import Reporter, ReportersRes
from ..utils.auth import current_user
from ..utils.reporter import REPORTERS_DB

# Create a FastAPI router with a prefix for reporter-related endpoints
router = APIRouter(prefix="/reporter", tags=["Reporter"])


@router.get("/all", response_model=ReportersRes)
async def get_reporters_all(
    pag: Annotated[
        PaginationQueryParams, Depends(PaginationQueryParams)
    ],  # Pagination parameters
    auth: Annotated[Reporter, Depends(current_user)],  # Current authenticated user
):
    """
    Retrieve all reporters with optional pagination.

    This endpoint returns a list of all reporters, with optional pagination
    specified by 'skip' and 'limit'. It uses dependency injection to get pagination
    parameters and the current authenticated user.
    """

    # Retrieve all reporters from the database and apply pagination if needed
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
