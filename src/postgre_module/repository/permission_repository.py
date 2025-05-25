from typing import Optional
from uuid import UUID

from postgre_module.models import Permission
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class PermissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Optional[Permission]:
        stmt = select(Permission).where(Permission.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, name: str) -> Optional[Permission]:
        stmt = select(Permission).where(Permission.name == name).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, name: str):
        perm = Permission(name=name)
        self.session.add(perm)
        await self.session.flush()
        return await self.get_by_id(perm.id)