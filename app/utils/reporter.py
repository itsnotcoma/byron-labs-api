from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends

from ..models.reporter import (
    Reporter,
    ReporterDTO,  # Models for reporters
    ReporterQueryParams,
)


def search_reporter_db(username: str):
    """
    Search for a reporter in the database by username.

    This function returns a `ReporterDTO` if the username exists in `REPORTERS_DB`.
    If the username does not exist, it returns `None`.
    """
    if username in REPORTERS_DB:
        return ReporterDTO(**REPORTERS_DB[username])


def search_reporter(username: str):
    """
    Search for a basic reporter in the database by username.

    This function returns a `Reporter` if the username exists in `REPORTERS_DB`.
    If the username does not exist, it returns `None`.
    """
    if username in REPORTERS_DB:
        return Reporter(**REPORTERS_DB[username])


def search_reporters_by_query(
    q: Annotated[ReporterQueryParams, Depends(ReporterQueryParams)]
):
    """
    Search for reporters based on query parameters.

    This function filters the `REPORTERS_DB` based on the query parameters
    provided by `ReporterQueryParams`. It supports filtering by first name,
    last name, username, and company.
    """
    filtered_reporters = REPORTERS_DB

    if q.first_name:
        filtered_reporters = [
            reporter
            for reporter in REPORTERS_DB.values()
            if q.first_name.lower() in reporter.name.lower()
        ]

    if q.last_name:
        filtered_reporters = [
            reporter
            for reporter in filtered_reporters
            if q.last_name.lower() in reporter.name.lower()
        ]

    if q.username:
        filtered_reporters = [
            reporter
            for reporter in filtered_reporters
            if reporter.username == q.username
        ]

    if q.company:
        filtered_reporters = [
            reporter
            for reporter in filtered_reporters
            if q.company.lower() in reporter.company.lower()
        ]

    return filtered_reporters


# A mock database of reporters with sample data for testing and development
REPORTERS_DB = {
    "john.doe": {
        "id": uuid4(),
        "username": "john.doe",
        "name": "John Doe",
        "email": "john.doe@mail.com",
        "password": "$2a$12$haRs4/ppy4hvfTCNNOwX6eUBz5Wjk88bCLjcQcd6meaKkpGWQoc.C",
        "company": "Byron Labs",
        "disabled": False,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
    "jane.doe": {
        "id": uuid4(),
        "username": "jane.doe",
        "name": "Jane Doe",
        "email": "jane.doe@mail.com",
        "password": "$2a$12$haRs4/ppy4hvfTCNNOwX6eUBz5Wjk88bCLjcQcd6meaKkpGWQoc.C",
        "company": "Cyberdyne Systems",
        "disabled": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    },
}
