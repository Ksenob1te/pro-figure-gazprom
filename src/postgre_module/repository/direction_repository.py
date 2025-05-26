from uuid import UUID
from postgre_module.models import HackathonDirection
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HackathonDirectionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> HackathonDirection | None:
        stmt = select(HackathonDirection).where(HackathonDirection.id == id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[HackathonDirection]:
        stmt = select(HackathonDirection)
        return list((await self.session.scalars(stmt)).all())
    
    async def create(self, name: str) -> HackathonDirection:
        direction = HackathonDirection(name=name)
        self.session.add(direction)
        await self.session.flush()
        return direction