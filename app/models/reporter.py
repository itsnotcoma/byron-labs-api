from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel


class Reporter(BaseModel):
    """
    Basic model representing a reporter.

    This class includes the basic information about a reporter, such as
    username, name, email, and company.
    """

    username: str  # Reporter's username
    name: str  # Reporter's full name
    email: str  # Reporter's email address
    company: str  # Company the reporter is associated with


class ReporterDTO(Reporter):
    """
    Extended reporter model for Data Transfer Object (DTO) purposes.

    This class extends the base Reporter model with additional information
    such as unique identifiers, password, account status, and timestamps.
    """

    id: UUID  # Unique identifier for the reporter
    password: str  # Password for authentication (sensitive data)
    disabled: bool  # Whether the reporter's account is disabled
    created_at: datetime  # Timestamp for when the reporter was created
    updated_at: datetime  # Timestamp for when the reporter was last updated


class ReportersRes(BaseModel):
    """
    Response model for returning a list of reporters.

    This class contains a list of ReporterDTO objects and additional metadata
    about the total count of reporters, the number of skipped records, and the limit on the returned data.
    """

    data: list[ReporterDTO]  # List of reporter data transfer objects
    total: int  # Total number of reporters
    skip: int  # Number of records skipped (for pagination)
    limit: int  # Limit on the number of records returned


class ReporterQueryParams:
    """
    Query parameters for filtering reporters.

    This class defines the expected query parameters for endpoints that
    manage reporters, allowing filtering based on attributes such as first name,
    last name, username, and company.
    """

    def __init__(
        self,
        first_name: Annotated[str, Query()] = None,  # Filter by first name
        last_name: Annotated[str, Query()] = None,  # Filter by last name
        username: Annotated[str, Query()] = None,  # Filter by username
        company: Annotated[str, Query()] = None,  # Filter by company
    ):
        self.first_name = first_name  # Reporter's first name
        self.last_name = last_name  # Reporter's last name
        self.username = username  # Reporter's username
        self.company = company  # Company associated with the reporter
