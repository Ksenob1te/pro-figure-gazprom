from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import TeamAchievement
from uuid import UUID
import logging


# TeamAchievement(id: UUID, league_id: UUID, team_id: UUID, gameweek_id: UUID, icon: str)
class TeamAchievementRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_id(self, team_achievement_id: UUID) -> TeamAchievement | None:
        stmt = select(TeamAchievement).where(TeamAchievement.id == team_achievement_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, league_id: UUID, team_id: UUID, gameweek_id: UUID, icon: str) -> TeamAchievement:
        team_achievement = TeamAchievement(league_id=league_id, team_id=team_id, gameweek_id=gameweek_id, icon=icon)
        self.session.add(team_achievement)
        await self.session.flush()
        return await self.get_by_id(team_achievement.id)

    async def set_icon(self, team_achievement: TeamAchievement, icon: str) -> TeamAchievement:
        team_achievement.icon = icon
        await self.session.flush()
        return team_achievement
