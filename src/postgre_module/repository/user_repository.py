from uuid import UUID
from postgre_module.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID):
        stmt = select(User).where(User.id == id)
        return await self.session.scalar(stmt)
    
    async def get_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        return await self.session.scalar(stmt)

    async def set_password(self, user: User, password: str, flush=True):
        user.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if flush:
            await self.session.flush()

    async def check_password(self, user: User, password: str):
        return bcrypt.checkpw(password.encode(), user.hashed_password.encode())

    async def create(self, username: str, password: str):
        user = User(username=username)
        await self.set_password(user, password)
        self.session.add(user)
        await self.session.flush()