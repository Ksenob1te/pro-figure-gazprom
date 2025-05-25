from backend.api.auth.models import LogInRequest, SignUpRequest, UserInfo
from backend.utils import GetDBSession, GetOptionalUser, GetRedisClient, GetUser
from domain.services.user.service import UserService
from fastapi import Response
from fastapi_controllers import Controller, get, post
from postgre_module.repository.user_repository import UserRepository
from redis_module.repository import RedisRepository
from domain.services.user.models import LogInRequest as DomainLogInRequest, SignUpRequest as DomainSignUpRequest
from settings import APP_SETTINGS

class UserController:
    prefix = "/user"
    tags = ["user"]

    def __init__(self, session: GetDBSession, redis: GetRedisClient) -> None:
        super().__init__()
        user_repository = UserRepository(session)
        redis_repository = RedisRepository(redis)

        self.user_service = UserService(user_repository, redis_repository)
