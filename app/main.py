from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import config
from .routers import auth, incident, reporter

# Initialize the FastAPI application
app = FastAPI()

# Include routers for various parts of the application
app.include_router(auth.router)  # Authentication and user-related endpoints
app.include_router(incident.router)  # Incident management endpoints
app.include_router(reporter.router)  # Reporter-related endpoints

# Configure Cross-Origin Resource Sharing (CORS) to allow specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # Allow all origins for development purposes
    allow_credentials=True,  # Allow use of cookies and HTTP authentication with CORS
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


# A basic endpoint to check the status of the application
@app.get("/")
async def get_status(
    settings: Annotated[
        config.Settings, Depends(config.get_settings)
    ]  # Inject configuration settings
):
    """Returns a basic status check, including the application name and version."""
    return {
        "status": "OK",  # Indicates the application is running properly
        "name": settings.app_name,  # Name of the application
        "version": "0.1",  # Application version number
    }
