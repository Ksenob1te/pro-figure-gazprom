from backend.utils import GetDBSession, GetOptionalUser, GetRedisClient, GetUser
from domain.services.achievements import *
from fastapi import Response
from fastapi_controllers import Controller, get, post
from postgre_module import AchievementRepository, UserStatsRepository, Achievement
from .models import *
from settings import APP_SETTINGS

class AchievementController(Controller):
    prefix = "/achievement"
    tags = ["achievement"]

    def __init__(self, session: GetDBSession) -> None:
        super().__init__()
        achievement_repository = AchievementRepository(session)
        user_stats_repository = UserStatsRepository(session)

        self.user_service = AchievementService(achievement_repository, user_stats_repository)

    @get("/", response_model=AchievementsInfo)
    async def get_user_achievements(self, user: GetUser):
        user_stats = self.user_service.get_create_user_stats(user.user_id)
        user_achievements =  self.user_service.get_user_achievements(user.user_id)
        unearned_achievements = self.user_service.get_unearned_achievements(user.user_id)
        return {"user": await user_stats, "unlocked_achievements": await user_achievements,
                "locked_achievements": await unearned_achievements}

    @post("/create")
    async def create_achievement(self, data: AchievementRequest):
        achievement = await self.user_service.create_achievement(data)
        return {"message": "Achievement created successfully", "achievement": achievement}

    @get("/id/{achievement_code}", response_model=AchievementsFullData)
    async def get_achievement_by_id(self, achievement_code: str):
        achievement = await self.user_service.get_achievement_by_code(achievement_code)
        if not achievement:
            raise AchievementNotFound(f"Achievement with id {achievement_code} not found")
        return achievement

    @post("/grant/{achievement_code}")
    async def assign_achievement(self, achievement_code: str, user: GetUser):
        achievement = await self.user_service.get_achievement_by_code(achievement_code)

        await self.user_service.grant_achievement(user.user_id, achievement.code)
        return {"message": f"Achievement {achievement.name} assigned to user {user.user_id}"}
