from typing import Optional
from uuid import UUID
from postgre_module.models import Permission, Role, RolePerm
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from .. import Achievement, UserAchievement, UserStats
import datetime
import math


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    
    async def get_by_id(self, id: UUID) -> Optional[Role]:
        stmt = select(Role).where(Role.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_default(self) -> Optional[Role]:
        return await self.get_by_name("User")

    async def get_all(self) -> list[Role]:
        stmt = select(Role)
        return list((await self.session.scalars(stmt)).all())

    async def create(self, name: str, flush=True):
        role = Role(name=name)
        self.session.add(role)
        if flush:
            await self.session.flush()

    async def add_permission(self, role: Role, permission: Permission):
        role_perm = RolePerm(role_id=role.id, perm_id=permission.id)
        self.session.add(role_perm)
        await self.session.flush()

    async def get_permissions(self, role: Role) -> list[Permission]:
        stmt = select(RolePerm).where(RolePerm.role_id == role.id)
        role_perms = (await self.session.scalars(stmt)).all()
        perms = []
        for i in role_perms:
            perms.append(i.perm)
        return perms

    async def check_permission(self, role: Role, permission: Permission) -> bool:
        stmt = select(RolePerm).where(RolePerm.role_id ==
                                      role.id, RolePerm.permission_id == permission.id).limit(1)
        result = await self.session.scalar(stmt)
        return result is not None