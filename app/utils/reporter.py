from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends

from ..models.reporter import QueryReporterParams, Reporter, ReporterDTO


def search_reporter_db(username: str):
    if username in REPORTERS_DB:
        return ReporterDTO(**REPORTERS_DB[username])


def search_reporter(username: str):
    if username in REPORTERS_DB:
        return Reporter(**REPORTERS_DB[username])


def search_reporters_by_query(
    q: Annotated[QueryReporterParams, Depends(QueryReporterParams)]
):
    filtered_reporters = REPORTERS_DB
    if q.first_name:
        filtered_reporters = [
            reporter
            for reporter in REPORTERS_DB
            if q.first_name.lower() in reporter.first_name.lower()
        ]

    if q.last_name:
        filtered_reporters = [
            reporter
            for reporter in filtered_reporters
            if q.last_name.lower() in reporter.last_name.lower()
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
