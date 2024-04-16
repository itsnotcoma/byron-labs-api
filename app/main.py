from typing import Annotated

from fastapi import Depends, FastAPI

from .core import config
from .routers import auth, incident, reporter

app = FastAPI()

app.include_router(auth.router)
app.include_router(incident.router)
app.include_router(reporter.router)


@app.get("/")
async def get_status(
    settings: Annotated[config.Settings, Depends(config.get_settings)]
):
    return {
        "status": "OK",
        "name": settings.app_name,
        "version": "0.1",
    }
