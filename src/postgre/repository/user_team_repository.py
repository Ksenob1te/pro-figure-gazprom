from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import UserTeam
from uuid import UUID
import logging


class UserTeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, user_team_id: UUID) -> UserTeam | None:
        stmt = select(UserTeam).where(UserTeam.id == user_team_id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user_id: UUID) -> UserTeam | None:
        stmt = select(UserTeam).where(UserTeam.user_id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user_id: UUID, team_id: UUID) -> UserTeam:
        user_team = UserTeam(user_id=user_id,
                             team_id=team_id)
        self.session.add(user_team)
        await self.session.flush()
        self.logger.info(f"UserTeam {user_team.id} created (user_id: {user_team.user_id},"
                         f" team_id: {user_team.team_id}), id: {user_team.id}")
        return await self.get_by_id(user_team.id)

