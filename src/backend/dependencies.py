from typing import Annotated
from backend.utils import GetDBSession, GetRedisClient
from domain.services.achievements.service import AchievementService
from domain.services.user.service import UserService
from fastapi import Depends
from postgre_module.repository.achievement_repository import AchievementRepository
from postgre_module.repository.permission_repository import PermissionRepository
from postgre_module.repository.role_repository import RoleRepository
from postgre_module.repository.user_repository import UserRepository
from postgre_module.repository.user_stats_repository import UserStatsRepository
from redis_module.repository import RedisRepository


def get_user_repository(session: GetDBSession):
    return UserRepository(session)

def get_achievement_repository(session: GetDBSession):
    return AchievementRepository(session)

def get_permission_repository(session: GetDBSession):
    return PermissionRepository(session)

def get_role_repository(session: GetDBSession):
    return RoleRepository(session)

def get_user_stats_repository(session: GetDBSession):
    return UserStatsRepository(session)

def get_redis_repository(redis_session: GetRedisClient):
    return RedisRepository(redis_session)

def get_user_service(user_repository=Depends(get_user_repository),
                     redis_repository=Depends(get_redis_repository),
                     role_repository=Depends(get_role_repository),
                     ):
    return UserService(user_repository,
                       redis_repository,
                       role_repository)

def get_achievement_service(achievement_repository=Depends(get_achievement_repository),
                            user_stats_repository=Depends(get_user_stats_repository)):
    return AchievementService(achievement_repository, user_stats_repository)

UserServiceDepends = Annotated[UserService, Depends(get_user_service)]
AchievementServiceDepends = Annotated[AchievementService, Depends(get_achievement_service)]