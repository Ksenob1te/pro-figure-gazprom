from uuid import UUID
from postgre_module.models import Solution
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class SolutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Solution | None:
        stmt = select(Solution).where(Solution.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def get_by_hackathon_id(self, hackathon_id: UUID) -> Solution | None:
        stmt = select(Solution).where(Solution.hackathon_id == hackathon_id).limit(1)
        return await self.session.scalar(stmt)
    
    