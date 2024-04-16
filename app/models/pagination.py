from typing import Annotated

from fastapi import Query


class QueryPaginationParams:
    def __init__(
        self, skip: Annotated[int, Query()] = 0, limit: Annotated[int, Query()] = 12
    ):
        self.skip = skip
        self.limit = limit
