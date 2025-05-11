from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Team
from uuid import UUID
import logging


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, team_id: UUID) -> Team | None:
        stmt = select(Team).where(Team.id == team_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_entry(self, entry: int) -> Team | None:
        stmt = select(Team).where(Team.entry == entry).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, entry: int, name: str, leader: str, pts_total: int, pts_gw: int) -> Team:
        team = Team(entry=entry,
                    name=name,
                    leader=leader,
                    pts_total=pts_total,
                    pts_gw=pts_gw)
        self.session.add(team)
        await self.session.flush()
        self.logger.info(f"Team {team.name} created (entry: {team.entry}), id: {team.id}")
        return await self.get_by_id(team.id)

    async def set_pts_total(self, team: Team, pts_total: int) -> Team:
        team.pts_total = pts_total
        await self.session.flush()
        return team

    async def set_pts_gw(self, team: Team, pts_gw: int) -> Team:
        team.pts_gw = pts_gw
        await self.session.flush()
        return team

    async def set_players_played(self, team: Team, players_played: int) -> Team:
        team.players_played = players_played
        await self.session.flush()
        return team

    async def set_pick(self, team: Team, match_id: int, pick: int) -> Team:
        tmp_pick = team.pick.copy()
        tmp_pick[str(match_id)] = pick
        team.pick = tmp_pick
        await self.session.flush()
        return team

    async def set_picks(self, team: Team, picks: Dict[int, int]) -> Team:
        picks: Dict[str, int] = {str(k): v for k, v in picks.items()}
        team.pick = picks
        await self.session.flush()
        return team

    @staticmethod
    async def get_pick(team: Team, match_id: int) -> int | None:
        return team.pick.get(str(match_id), None)
