from typing import Annotated

from fastapi import Query


class SortOrder:
    """
    Defines possible sort orders.

    This class provides constants for ascending (`ASC`) and descending (`DESC`) sort orders.
    These are used to indicate the direction in which results should be sorted.
    """

    ASC = "asc"  # Ascending sort order
    DESC = "desc"  # Descending sort order


class SortQueryParams:
    """
    Query parameters for sorting results.

    This class is used to define query parameters for sorting results in
    FastAPI endpoints. It includes the field by which to sort and the order
    (ascending or descending).
    """

    def __init__(
        self,
        sort_by: Annotated[
            str, Query()
        ] = "created_by",  # Field to sort by (default is 'created_by')
        sort_order: Annotated[int, Query()] = -1,  # Sort order (default is descending)
    ):
        self.sort_by = sort_by  # Attribute to sort results by
        self.sort_order = sort_order  # Sort order (1 for ascending, -1 for descending)
