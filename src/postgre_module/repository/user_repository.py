from uuid import UUID
from postgre_module.models import Role, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> User | None:
        stmt = select(User).where(User.id == id)
        return await self.session.scalar(stmt)
    
    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return await self.session.scalar(stmt)

    async def set_password(self, user: User, password: str, flush=True):
        user.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        if flush:
            await self.session.flush()

    async def check_password(self, user: User, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), user.hashed_password.encode())

    async def create(self, username: str, password: str, role: Role):
        user = User(username=username, role_id=role.id)
        await self.set_password(user, password)
        self.session.add(user)
        await self.session.flush()