from uuid import UUID

from postgre_module.models import UserAchievement

from src.postgre_module import AchievementRepository, UserStatsRepository
from src.postgre_module import UserStats, Achievement
from .exceptions import (
    AchievementAlreadyEarned,
    AchievementNotFound,
    UserStatsNotFound,
    AchievementAlreadyExists,
    UserStatsAlreadyExists
)
from .models import *


class AchievementService:
    def __init__(
        self,
        achievement_repository: AchievementRepository,
        user_stats_repository: UserStatsRepository,
    ):
        self.achievement_repository = achievement_repository
        self.user_stats_repository = user_stats_repository

    async def get_achievement_by_id(self, achievement_id: UUID) -> Achievement:
        achievement = await self.achievement_repository.get_by_id(achievement_id)
        if not achievement:
            raise AchievementNotFound(f"Achievement with id {achievement_id} not found")
        return achievement

    async def get_achievement_by_code(self, achievement_code: str) -> Achievement:
        achievement = await self.achievement_repository.get_by_code(achievement_code)
        if not achievement:
            raise AchievementNotFound(f"Achievement with code '{achievement_code}' not found")
        return achievement

    async def get_create_user_stats(self, user_id: UUID) -> UserStats:
        user_stats = await self.user_stats_repository.get_by_user_id(user_id)
        if not user_stats:
            user_stats_id = await self.user_stats_repository.create(user_id)
            user_stats = await self.user_stats_repository.get_by_id(user_stats_id)
        return user_stats

    async def get_user_stats(self, user_id: UUID) -> UserStats:
        user_stats = await self.user_stats_repository.get_by_user_id(user_id)
        if not user_stats:
            raise UserStatsNotFound(f"UserStats not found for user_id={user_id}")
        return user_stats

    async def create_achievement(self, achievement_data: AchievementRequest) -> Achievement:
        existing = await self.achievement_repository.get_by_code(achievement_data.code)
        if existing:
            raise AchievementAlreadyExists(f"Achievement with code '{achievement_data.code}' already exists")

        achievement_id = await self.achievement_repository.create(
            code=achievement_data.code, name=achievement_data.name, description=achievement_data.description,
            experience_reward=achievement_data.experience_reward, is_hidden=achievement_data.is_hidden
        )
        achievement = await self.achievement_repository.get_by_id(achievement_id)
        return achievement

    async def create_user_stats(self, user_id: UUID) -> UserStats:
        existing_stats = await self.user_stats_repository.get_by_user_id(user_id)
        if existing_stats:
            raise UserStatsAlreadyExists(f"UserStats already exists for user_id={user_id}")

        user_stats_id = await self.user_stats_repository.create(user_id)
        user_stats = await self.user_stats_repository.get_by_id(user_stats_id)
        return user_stats

    async def grant_achievement(self, user_id: UUID, achievement_code: str, level: str) -> None:
        user_stats = await self.get_user_stats(user_id)

        achievement = await self.achievement_repository.get_by_code(achievement_code)
        if not achievement:
            raise AchievementNotFound(f"Achievement with code '{achievement_code}' not found")

        already_earned = await self.achievement_repository.has_user_achievement(user_stats.id, achievement.id, level)
        if already_earned:
            raise AchievementAlreadyEarned(f"User already has achievement '{achievement_code}'")

        await self.achievement_repository.grant_achievement(user_stats, achievement, level=level)
        user_stats.experience += achievement.experience_reward
        await self.achievement_repository.update_level(user_stats)
        return None

    async def get_user_achievements(self, user_id: UUID) -> list[UserAchievement]:
        user_stats = await self.get_user_stats(user_id)
        return await self.achievement_repository.get_user_achievements_list(user_stats.id)

    async def get_unearned_achievements(self, user_id: UUID) -> list[Achievement]:
        user_stats = await self.get_user_stats(user_id)
        return await self.achievement_repository.get_unearned_achievements(user_stats.id)