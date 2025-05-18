from fastapi import FastAPI
from backend.api import router

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='Gazpromic',
    version="0.1",
)

app.include_router(router)