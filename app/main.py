from fastapi import FastAPI

from .routers import auth, incident, reporter

app = FastAPI()

app.include_router(auth.router)
app.include_router(incident.router)
app.include_router(reporter.router)


@app.get("/")
async def get_status():
    return {"status": "OK"}
