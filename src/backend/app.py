from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.api import router
from redis_module.service import free_redis_pool, setup_redis_pool

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='Gazpromic',
    version="0.1",
)

app.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_redis_pool()
    yield
    await free_redis_pool()