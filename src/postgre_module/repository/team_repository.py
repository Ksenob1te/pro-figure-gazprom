from uuid import UUID
from postgre_module.models import Hackathon, Team
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Team | None:
        stmt = select(Team).where(Team.id == id).limit(1)
        return await self.session.scalar(stmt)
    
    async def create(self, name: str, hackathon_id: UUID, leader_id: UUID):
        team = Team(name=name, hackathon_id=hackathon_id, leader_id=leader_id)
        self.session.add(team)
        await self.session.flush()

    