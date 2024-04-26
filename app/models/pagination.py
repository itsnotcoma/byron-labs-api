from typing import Annotated  # Allows for additional metadata in type annotations

from fastapi import Query  # FastAPI Query parameter handling


class PaginationQueryParams:
    """
    Query parameters for pagination in API requests.

    This class defines the expected query parameters used for pagination,
    allowing the specification of 'skip' and 'limit' for controlling which records
    are retrieved and how many.
    """

    def __init__(
        self,
        skip: Annotated[
            int | None, Query()
        ] = 0,  # Number of records to skip (default 0)
        limit: Annotated[
            int | None, Query()
        ] = None,  # Maximum number of records to return
    ):
        self.skip = skip  # How many records to skip
        self.limit = limit  # Maximum number of records to return
