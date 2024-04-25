from typing import Annotated

from fastapi import Query


class QueryPaginationParams:
    def __init__(
        self,
        skip: Annotated[int | None, Query()] = 0,
        limit: Annotated[int | None, Query()] = None,
    ):
        self.skip = skip
        self.limit = limit
