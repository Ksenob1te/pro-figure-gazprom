from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .. import Achievement, UserAchievement, UserStats
import datetime
import math


class AchievementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, achievement_id: UUID) -> Achievement | None:
        stmt = select(Achievement).where(Achievement.id == achievement_id)
        return await self.session.scalar(stmt)

    async def get_by_code(self, code: str) -> Achievement | None:
        stmt = select(Achievement).where(Achievement.code == code)
        return await self.session.scalar(stmt)

    async def has_user_achievement(self, user_stats_id: UUID, achievement_id: UUID, level: str) -> bool:
        stmt = select(UserAchievement).where(
            and_(
                UserAchievement.user_stats_id == user_stats_id,
                UserAchievement.achievement_id == achievement_id,
                UserAchievement.level == level
            )
        )
        result = await self.session.scalar(stmt)
        return result is not None

    async def grant_achievement(self, user_stats: UserStats, achievement: Achievement, level: str) -> bool:
        if await self.has_user_achievement(user_stats.id, achievement.id, level):
            return False

        user_achievement = UserAchievement(
            user_stats_id=user_stats.id,
            achievement_id=achievement.id,
            level=level
        )
        self.session.add(user_achievement)
        await self.session.flush()
        return True

    async def get_user_achievements(self, user_stats_id: UUID) -> list[UserAchievement]:
        stmt = select(UserAchievement).where(UserAchievement.user_stats_id == user_stats_id)
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_user_achievements_list(self, user_stats_id: UUID) -> list[UserAchievement]:
        stmt = (
            select(UserAchievement)
            .where(UserAchievement.user_stats_id == user_stats_id)
        )
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_unearned_achievements(self, user_stats_id: UUID) -> list[Achievement]:
        earned_stmt = select(UserAchievement.achievement_id).where(UserAchievement.user_stats_id == user_stats_id)
        stmt = select(Achievement).where(~Achievement.id.in_(earned_stmt))
        result = await self.session.scalars(stmt)
        return list(result)

    @staticmethod
    async def _exp_to_level(level: int, base: int = 100, growth: float = 1.5, max_level: int = 100) -> int:
        level = max(1, min(level, max_level))
        return int(base * ((growth ** (level - 1)) - 1) / (growth - 1))

    @staticmethod
    async def level_from_exp(exp: int, base: int = 100, growth: float = 1.5, max_level: int = 100) -> int:
        if exp <= 0:
            return 1

        level = math.log(1 + (exp * (growth - 1)) / base, growth) + 1
        level = int(level)

        return min(level, max_level)

    async def update_level(self, user_stats: UserStats, base: int = 100, growth: float = 1.5) -> None:
        level = await self.level_from_exp(user_stats.experience, base=base, growth=growth)
        user_stats.level = level
        await self.session.flush()

    async def create(self, code: str, name: str, description: str,
                     experience_reward: int = 0, is_hidden: bool = False, flush: bool = True) -> UUID:
        achievement = Achievement(
            code=code, name=name, description=description,
            experience_reward=experience_reward, is_hidden=is_hidden
        )
        self.session.add(achievement)
        if flush:
            await self.session.flush()
        return achievement.id
