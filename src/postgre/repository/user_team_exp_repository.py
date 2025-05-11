from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import UserTeamExpansion
from uuid import UUID
import logging


# UserTeamExpansion(id: UUID, user_team_id: UUID, league_id: UUID)

class UserTeamExpRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, user_team_exp_id: UUID) -> UserTeamExpansion | None:
        stmt = select(UserTeamExpansion).where(UserTeamExpansion.id == user_team_exp_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user_team_id: UUID, league_id: UUID) -> UserTeamExpansion:
        user_team_exp = UserTeamExpansion(user_team_id=user_team_id, league_id=league_id)
        self.session.add(user_team_exp)
        await self.session.flush()
        return await self.get_by_id(user_team_exp.id)