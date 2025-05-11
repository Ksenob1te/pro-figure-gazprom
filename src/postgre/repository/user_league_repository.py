from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import UserLeague
from uuid import UUID
import logging


class UserLeagueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, user_league_id: UUID) -> UserLeague | None:
        stmt = select(UserLeague).where(UserLeague.id == user_league_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user_id: UUID) -> UserLeague | None:
        stmt = select(UserLeague).where(UserLeague.user_id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def change_league(self, user_league_field: UserLeague, league_id: UUID) -> UserLeague:
        user_league_field.league_id = league_id
        await self.session.flush()
        return user_league_field

    async def create(self, user_id: UUID, league_id: UUID) -> UserLeague:
        user_league = UserLeague(user_id=user_id,
                                 league_id=league_id)
        self.session.add(user_league)
        await self.session.flush()
        self.logger.info(f"UserLeague {user_league.id} created (user_id: {user_league.user_id},"
                         f" league_id: {user_league.league_id}), id: {user_league.id}")
        return await self.get_by_id(user_league.id)
