from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import GoatBoost
from uuid import UUID
import logging


# GoatBoost(id: UUID, goat_pick_id: UUID, boost_tag: str, match_id: int)
class GoatBoostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, goat_boost_id: UUID) -> GoatBoost | None:
        stmt = select(GoatBoost).where(GoatBoost.id == goat_boost_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, goat_pick_id: UUID, boost_tag: str, match_id: int) -> GoatBoost:
        goat_boost = GoatBoost(goat_pick_id=goat_pick_id, boost_tag=boost_tag, match_id=match_id)
        self.session.add(goat_boost)
        await self.session.flush()
        return await self.get_by_id(goat_boost.id)

    async def set_boost_tag(self, goat_boost: GoatBoost, boost_tag: str) -> GoatBoost:
        goat_boost.boost_tag = boost_tag
        await self.session.flush()
        return goat_boost

    async def set_match_id(self, goat_boost: GoatBoost, match_id: int) -> GoatBoost:
        goat_boost.match_id = match_id
        await self.session.flush()
        return goat_boost
