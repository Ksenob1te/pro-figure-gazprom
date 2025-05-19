from backend.api.auth.models import LogInRequest, SignUpRequest, UserInfo
from backend.utils import GetDBSession, GetOptionalUser, GetRedisClient, GetUser
from domain.services.user.service import UserService
from fastapi import Response
from fastapi_controllers import Controller, get, post
from postgre_module.repository.user_repository import UserRepository
from redis_module.repository import RedisRepository
from domain.services.user.models import LogInRequest as DomainLogInRequest, SignUpRequest as DomainSignUpRequest
from settings import APP_SETTINGS


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, session: GetDBSession, redis: GetRedisClient) -> None:
        super().__init__()
        user_repository = UserRepository(session)
        redis_repository = RedisRepository(redis)

        self.user_service = UserService(user_repository, redis_repository)

    @get("", response_model=UserInfo)
    async def get_user_info(self, user: GetUser):
        return UserInfo(user_id=user.user_id)

    @post("/login")
    async def login(self, data: LogInRequest, response: Response):
        result = await self.user_service.login(
            DomainLogInRequest(
                data.username,
                data.password)
        )
        response.set_cookie("token",
                            result.token,
                            max_age=APP_SETTINGS.ttl.auth_token_expire,
                            httponly=True)
        return {"message": "OK"}

    @post("/logout")
    async def logout(self, user: GetUser):
        await self.user_service.logout(user.token)

    @post("/registration")
    async def registration(self, data: SignUpRequest):
        await self.user_service.signup(DomainSignUpRequest(
            data.username,
            data.password,
            data.repeat_password
        ))
        return {"message": "OK"}
