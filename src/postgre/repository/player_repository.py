from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Players
from uuid import UUID
import logging
from enum import Enum


class PlayerPosition(int, Enum):
    UNDEFINED = 0
    GK = 1
    DEF = 2
    MID = 3
    FWD = 4


class PlayerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: UUID) -> Players | None:
        stmt = select(Players).where(Players.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_static_id(self, id: int) -> Players | None:
        stmt = select(Players).where(Players.static_id == id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, static_id: int, name: str, points: int) -> Players:
        player_field = Players(static_id=static_id, name=name, points=points)
        self.session.add(player_field)
        await self.session.flush()
        self.logger.info(f"Player {player_field.id} created (static_id: {player_field.static_id}, name: {player_field.name})")
        return await self.get_by_id(player_field.id)

    async def set_real_name(self, player: Players, real_name: str) -> Players:
        player.real_name = real_name
        await self.session.flush()
        return player

    async def set_points(self, player: Players, points: int) -> Players:
        player.points = points
        await self.session.flush()
        return player

    async def set_team(self, player: Players, team: str) -> Players:
        player.team = team
        await self.session.flush()
        return player

    async def set_position(self, player: Players, position: int) -> Players:
        player.position = position
        await self.session.flush()
        return player

    @staticmethod
    async def get_position(player: Players) -> PlayerPosition:
        return PlayerPosition(player.position)

    async def set_player_price(self, player: Players, price: int) -> Players:
        player.price = price
        await self.session.flush()
        return player

    async def set_played(self, player: Players, played: bool) -> Players:
        player.played = played
        await self.session.flush()
        return player

    async def set_status(self, player: Players, status: str) -> Players:
        player.status = status
        await self.session.flush()
        return player

    async def set_news(self, player: Players, news: str) -> Players:
        player.news = news
        await self.session.flush()
        return player

    async def set_photo(self, player: Players, photo: str) -> Players:
        player.photo = photo
        await self.session.flush()
        return player


