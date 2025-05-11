import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Match
from uuid import UUID
import logging


# Match(id: UUID, match_id: int, gameweek_id: UUID, finished: bool, finished_provisional: bool,
# kickoff_time: datetime, first_team: str, second_team: str)
class MatchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, match_id: UUID) -> Match | None:
        stmt = select(Match).where(Match.id == match_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, match_id: int, gameweek_id: UUID, kickoff_time: datetime.datetime,
                     first_team: str, second_team: str) -> Match:
        match = Match(match_id=match_id, gameweek_id=gameweek_id, kickoff_time=kickoff_time,
                      first_team=first_team, second_team=second_team)
        self.session.add(match)
        await self.session.flush()
        return await self.get_by_id(match.id)

    async def set_finished(self, match: Match, finished: bool) -> Match:
        match.finished = finished
        await self.session.flush()
        return match

    async def set_finished_provisional(self, match: Match, finished_provisional: bool) -> Match:
        match.finished_provisional = finished_provisional
        await self.session.flush()
        return match

    async def set_kickoff_time(self, match: Match, kickoff_time: datetime.datetime) -> Match:
        match.kickoff_time = kickoff_time
        await self.session.flush()
        return match

    async def set_first_team(self, match: Match, first_team: str) -> Match:
        match.first_team = first_team
        await self.session.flush()
        return match

    async def set_second_team(self, match: Match, second_team: str) -> Match:
        match.second_team = second_team
        await self.session.flush()
        return match
