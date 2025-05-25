from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .. import Achievement, UserAchievement, UserStats
import datetime
import math


class UserStatsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_stats_id: UUID) -> UserStats | None:
        stmt = select(UserStats).where(UserStats.id == user_stats_id)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user_id: UUID) -> UserStats | None:
        stmt = select(UserStats).where(UserStats.user_id == user_id)
        return await self.session.scalar(stmt)

    async def create(self, user_id: UUID) -> UUID:
        user_stats = UserStats(user_id=user_id)
        self.session.add(user_stats)
        await self.session.flush()
        return user_stats.id