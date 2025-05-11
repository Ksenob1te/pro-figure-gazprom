from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import LeagueExtendedExpansion
from uuid import UUID
import logging


# LeagueExtended (id: UUID, league_id: UUID, team_id: UUID, place: int)
class LeagueExtendedRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, league_extended_id: UUID) -> LeagueExtendedExpansion | None:
        stmt = select(LeagueExtendedExpansion).where(LeagueExtendedExpansion.id == league_extended_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, league_id: UUID, team_id: UUID, place: int) -> LeagueExtendedExpansion:
        league_extended = LeagueExtendedExpansion(league_id=league_id, team_id=team_id, place=place)
        self.session.add(league_extended)
        await self.session.flush()
        return await self.get_by_id(league_extended.id)

    async def set_place(self, league_extended: LeagueExtendedExpansion, place: int) -> LeagueExtendedExpansion:
        league_extended.place = place
        await self.session.flush()
        return league_extended
