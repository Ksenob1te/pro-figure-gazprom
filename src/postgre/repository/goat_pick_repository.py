from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import GoatPick
from uuid import UUID
from typing import List
import logging


class GoatPickRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: UUID) -> GoatPick | None:
        stmt = select(GoatPick).where(GoatPick.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user_goat_id: UUID, goat_gameweek_id: UUID) -> GoatPick:
        goat_pick = GoatPick(user_goat_id=user_goat_id, goat_gameweek_id=goat_gameweek_id)
        self.session.add(goat_pick)
        await self.session.flush()
        self.logger.info(f"GoatPick {goat_pick.id} created (user_id: {goat_pick.user_goat_id}, gameweek_id: {goat_pick.goat_gameweek_id})")
        return await self.get_by_id(goat_pick.id)

    async def set_bps(self, goat_pick: GoatPick, bps: int) -> GoatPick:
        goat_pick.bps = bps
        await self.session.flush()
        return goat_pick

    async def set_pick(self, goat_pick: GoatPick, pick: List[int]) -> GoatPick:
        goat_pick.pick = pick
        await self.session.flush()
        return goat_pick

    async def set_submitted(self, goat_pick: GoatPick, submitted: bool) -> GoatPick:
        goat_pick.submitted = submitted
        await self.session.flush()
        return goat_pick
