from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import League
from uuid import UUID
from enum import Enum
from typing import List

import logging


class LeagueType(str, Enum):
    CLASSIC = "c"
    H2H = "h"
    EXTENDED_MARK = "e"
    CLASSIC_EXTENDED = "c" + EXTENDED_MARK
    H2H_EXTENDED = "h" + EXTENDED_MARK


class LeagueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, league_id: UUID) -> League | None:
        stmt = select(League).where(League.id == league_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_league_id(self, league_id: int) -> League | None:
        stmt = select(League).where(League.league_id == league_id).limit(1)
        return await self.session.scalar(stmt)

    @staticmethod
    async def is_extended(league: League) -> bool:
        if league.league_type[-1] == LeagueType.EXTENDED_MARK:
            return True
        return False

    async def create(self, league_id: int, league_name: str, league_type: str, league_data = None) -> League:
        if league_data is None:
            league_data = {}
        league = League(league_id=league_id,
                        league_name=league_name,
                        league_type=league_type,
                        league_data=league_data)
        self.session.add(league)
        await self.session.flush()
        self.logger.info(f"League {league.league_name} created (type: {league.league_type}), id: {league.id}")
        return await self.get_by_id(league.id)

    async def set_data(self, league: League, league_data: dict) -> League:
        league.league_data = league_data
        await self.session.flush()
        return league

    @staticmethod
    async def get_league_type(league: League) -> LeagueType:
        return LeagueType(league.league_type)

    @staticmethod
    async def check_type(league: League, league_type: LeagueType) -> bool:
        if league.league_type == league_type:
            return True
        return False

    @staticmethod
    async def check_type_in(league: League, league_type_list: List[LeagueType]) -> bool:
        if league.league_type in league_type_list:
            return True
        return False

