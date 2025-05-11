from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import User
from uuid import UUID
import logging


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_chat_id(self, chat_id: str) -> User | None:
        stmt = select(User).where(User.chat_id == chat_id).limit(1)
        return await self.session.scalar(stmt)

    @staticmethod
    async def get_full_name(user: User) -> str | None:
        if user.first_name is None or user.last_name is None:
            return None
        return f"{user.first_name} {user.last_name}"

    async def create(self, chat_id: str, username: str = None, first_name: str = None, last_name: str = None) -> User:
        user = User(chat_id=chat_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name)
        self.session.add(user)
        await self.session.flush()
        self.logger.info(f"User {user.id} created (chat_id: {user.chat_id}, username: {user.username})")
        return await self.get_by_id(user.id)

    async def set_media_update(self, user: User, state: bool) -> User:
        user.media_update = state
        await self.session.flush()
        return user

    async def set_price_update(self, user: User, state: bool) -> User:
        user.price_update = state
        await self.session.flush()
        return user

