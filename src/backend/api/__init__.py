from fastapi import APIRouter
from backend.api.auth.controller import AuthController
from .achievements import AchievementController

router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(AchievementController.create_router())