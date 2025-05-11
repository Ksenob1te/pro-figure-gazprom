from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import LeagueH2HExpansion
from uuid import UUID
import logging


# LeagueH2HExpansion (id: UUID, league_id: UUID, team_id: UUID, wins: int, draws: int, losses: int)
class LeagueH2HExpRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, league_h2h_exp_id: UUID) -> LeagueH2HExpansion | None:
        stmt = select(LeagueH2HExpansion).where(LeagueH2HExpansion.id == league_h2h_exp_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, league_id: UUID, team_id: UUID, wins: int = 0, draws: int = 0, losses: int = 0) -> LeagueH2HExpansion:
        league_h2h_exp = LeagueH2HExpansion(league_id=league_id, team_id=team_id, wins=wins, draws=draws, losses=losses)
        self.session.add(league_h2h_exp)
        await self.session.flush()
        return await self.get_by_id(league_h2h_exp.id)

    async def set_wins(self, league_h2h_exp: LeagueH2HExpansion, wins: int) -> LeagueH2HExpansion:
        league_h2h_exp.wins = wins
        await self.session.flush()
        return league_h2h_exp

    async def set_draws(self, league_h2h_exp: LeagueH2HExpansion, draws: int) -> LeagueH2HExpansion:
        league_h2h_exp.draws = draws
        await self.session.flush()
        return league_h2h_exp

    async def set_losses(self, league_h2h_exp: LeagueH2HExpansion, losses: int) -> LeagueH2HExpansion:
        league_h2h_exp.losses = losses
        await self.session.flush()
        return league_h2h_exp
