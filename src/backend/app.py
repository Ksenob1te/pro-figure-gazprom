from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.api import router
from redis_module.service import free_redis_pool, setup_redis_pool
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_redis_pool()
    yield
    await free_redis_pool()

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title='Gazpromic',
    version="0.1",
    middleware=[
        Middleware(CORSMiddleware,
                   allow_origins=[
                       "localhost:8000", "26.222.166.167:8000", "26.222.166.167", "localhost"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True)
    ],
    lifespan=lifespan
)

app.include_router(router)
