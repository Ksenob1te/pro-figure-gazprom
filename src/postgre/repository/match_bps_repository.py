from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import MatchBPS
from uuid import UUID
import logging


# MatchBPS (id: UUID, match_id: UUID, player_id: UUID, bps: int, minutes: int)
class MatchBPSRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, match_bps_id: UUID) -> MatchBPS | None:
        stmt = select(MatchBPS).where(MatchBPS.id == match_bps_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, match_id: UUID, player_id: UUID, bps: int, minutes: int) -> MatchBPS:
        match_bps = MatchBPS(match_id=match_id, player_id=player_id, bps=bps, minutes=minutes)
        self.session.add(match_bps)
        await self.session.flush()
        return await self.get_by_id(match_bps.id)

    async def set_bps(self, match_bps: MatchBPS, bps: int) -> MatchBPS:
        match_bps.bps = bps
        await self.session.flush()
        return match_bps

    async def set_minutes(self, match_bps: MatchBPS, minutes: int) -> MatchBPS:
        match_bps.minutes = minutes
        await self.session.flush()
        return match_bps
