from backend.dependencies import AchievementServiceDepends
from backend.utils import  GetUser
from domain.services.achievements import *
from fastapi_controllers import Controller, get, post
from .models import *
from settings import APP_SETTINGS

class AchievementController(Controller):
    prefix = "/achievement"
    tags = ["achievement"]

    def __init__(self, achievement_service: AchievementServiceDepends) -> None:
        super().__init__()
        self.achievement_service = achievement_service

    @get("", response_model=AchievementsInfo)
    async def get_user_achievements(self, user: GetUser):
        user_stats = await self.achievement_service.get_create_user_stats(user.user_id)
        user_achievements = await self.achievement_service.get_user_achievements(user.user_id)
        unearned_achievements = await self.achievement_service.get_unearned_achievements(user.user_id)
        return {"user": user_stats, "unlocked_achievements": user_achievements,
                "locked_achievements": unearned_achievements}

    @post("/create")
    async def create_achievement(self, data: AchievementRequest):
        achievement = await self.achievement_service.create_achievement(data)
        return {"message": "Achievement created successfully", "achievement": achievement}

    @get("/id/{achievement_code}", response_model=AchievementsFullData)
    async def get_achievement_by_id(self, achievement_code: str):
        achievement = await self.achievement_service.get_achievement_by_code(achievement_code)
        if not achievement:
            raise AchievementNotFound(f"Achievement with id {achievement_code} not found")
        return achievement

    @post("/grant/{achievement_code}/{level}")
    async def assign_achievement(self, achievement_code: str, level: str, user: GetUser):
        achievement = await self.achievement_service.get_achievement_by_code(achievement_code)

        await self.achievement_service.grant_achievement(user.user_id, achievement.code, level=level)
        return {"message": f"Achievement {achievement.name} assigned to user {user.user_id}"}
