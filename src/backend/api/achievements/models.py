from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AchievementsFullData(BaseModel):
    class Config:
        orm_mode = True

    id: UUID
    code: str
    name: str
    description: str
    experience_reward: int
    is_hidden: bool


class AchievementsData(BaseModel):
    class Config:
        orm_mode = True

    id: UUID
    code: str
    name: str
    description: str
    experience_reward: int = 0

class UserAchievementsData(BaseModel):
    class Config:
        orm_mode = True
    level: str
    date_earned: datetime
    achievement: AchievementsData

class UserStatsData(BaseModel):
    class Config:
        orm_mode = True

    user_id: UUID
    level: int
    experience: int


class AchievementsInfo(BaseModel):
    class Config:
        orm_mode = True

    user: UserStatsData
    unlocked_achievements: list[UserAchievementsData]
    locked_achievements: list[AchievementsData]