from typing import Annotated

from fastapi import Query


class SortOrder:
    ASC = "asc"
    DESC = "desc"


class QuerySortParams:
    def __init__(
        self,
        sort_by: Annotated[str, Query()] = "created_by",
        sort_order: Annotated[int, Query()] = -1,
    ):
        self.sort_by = sort_by
        self.sort_order = sort_order
