from fastapi import APIRouter
from backend.api.auth.controller import AuthController

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())