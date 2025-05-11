from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import GoatGameweek
from uuid import UUID
import datetime
import logging

from config import configuration


class GoatGameweekRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: UUID) -> GoatGameweek | None:
        stmt = select(GoatGameweek).where(GoatGameweek.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_gameweek_id(self, gameweek_id: UUID) -> GoatGameweek | None:
        stmt = select(GoatGameweek).where(GoatGameweek.gameweek_id == gameweek_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, gameweek_id: UUID, subs_open: datetime.datetime, deadline: datetime.datetime, finish: datetime.datetime) -> GoatGameweek:
        goat_gameweek = GoatGameweek(gameweek_id=gameweek_id, subs_open=subs_open, deadline=deadline, finish=finish)
        self.session.add(goat_gameweek)
        await self.session.flush()
        self.logger.info(f"GoatGameweek {goat_gameweek.id} created (gameweek_id: {goat_gameweek.gameweek_id},"
                         f" subs_open: {goat_gameweek.subs_open}, deadline: {goat_gameweek.deadline}, finish: {goat_gameweek.finish})")
        return await self.get_by_id(goat_gameweek.id)

    async def set_finish(self, goat_gameweek: GoatGameweek, finish: datetime.datetime) -> GoatGameweek:
        goat_gameweek.finish = finish
        await self.session.flush()
        return goat_gameweek

    async def set_open_notification(self, goat_gameweek: GoatGameweek, open_notification: bool) -> GoatGameweek:
        goat_gameweek.open_notification = open_notification
        await self.session.flush()
        return goat_gameweek

    async def set_leaderboard_update(self, goat_gameweek: GoatGameweek, leaderboard_update: bool) -> GoatGameweek:
        goat_gameweek.leaderboard_update = leaderboard_update
        await self.session.flush()
        return goat_gameweek

    async def add_draft_notification(self, goat_gameweek: GoatGameweek, draft_notification: int) -> GoatGameweek:
        goat_gameweek.draft_notifications.append(draft_notification)
        await self.session.flush()
        return goat_gameweek

    async def process_bots_countdown(self, goat_gameweek: GoatGameweek) -> bool:
        goat_gameweek.bots_countdown -= 1
        if goat_gameweek.bots_countdown <= 0:
            goat_gameweek.bots_countdown = configuration.goat.bots_addition
            return True
        await self.session.flush()
        return False

