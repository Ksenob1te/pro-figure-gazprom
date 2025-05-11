from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import UserGoat
from uuid import UUID
import logging


class UserGoatRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, id: UUID) -> UserGoat | None:
        stmt = select(UserGoat).where(UserGoat.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user_id: UUID) -> UserGoat | None:
        stmt = select(UserGoat).where(UserGoat.user_id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user_id: UUID, name: str) -> UserGoat:
        user_goat = UserGoat(user_id=user_id, name=name)
        self.session.add(user_goat)
        await self.session.flush()
        self.logger.info(f"UserGoat {user_goat.id} created (user_id: {user_goat.user_id}, name: {user_goat.name})")
        return await self.get_by_id(user_goat.id)
