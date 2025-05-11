from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Gameweek
from uuid import UUID
import datetime
import logging

class GameweekRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: UUID) -> Gameweek | None:
        stmt = select(Gameweek).where(Gameweek.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_number(self, gameweek: int) -> Gameweek | None:
        stmt = select(Gameweek).where(Gameweek.gameweek == gameweek).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, gameweek: int, deadline: datetime.datetime, is_current: bool = False) -> Gameweek:
        gameweek = Gameweek(gameweek=gameweek, deadline=deadline, is_current=is_current)
        self.session.add(gameweek)
        await self.session.flush()
        self.logger.info(f"Gameweek {gameweek.id} created (number: {gameweek.gameweek}, deadline: {gameweek.deadline})")
        return await self.get_by_id(gameweek.id)

    async def set_current(self, gameweek: Gameweek, is_current: bool) -> Gameweek:
        gameweek.is_current = is_current
        await self.session.flush()
        self.logger.info(f"Gameweek {gameweek.id} set as current")
        return gameweek

    async def set_weekly_started(self, gameweek: Gameweek, weekly_started: bool) -> Gameweek:
        gameweek.weekly_started = weekly_started
        await self.session.flush()
        self.logger.info(f"Gameweek {gameweek.id} weekly update started")
        return gameweek

    async def set_intergame_started(self, gameweek: Gameweek, intergame_started: bool) -> Gameweek:
        gameweek.intergame_started = intergame_started
        await self.session.flush()
        self.logger.info(f"Gameweek {gameweek.id} intergame update started")
        return gameweek

    async def set_intergame_update(self, gameweek: Gameweek, intergame_finished: bool) -> Gameweek:
        gameweek.intergame_finished = intergame_finished
        await self.session.flush()
        self.logger.info(f"Gameweek {gameweek.id} intergame update finished")
        return gameweek