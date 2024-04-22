from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import config
from .routers import auth, incident, reporter

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3080",
]

app.include_router(auth.router)
app.include_router(incident.router)
app.include_router(reporter.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_status(
    settings: Annotated[config.Settings, Depends(config.get_settings)]
):
    return {
        "status": "OK",
        "name": settings.app_name,
        "version": "0.1",
    }
