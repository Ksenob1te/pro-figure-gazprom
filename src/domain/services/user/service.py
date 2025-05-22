from domain.services.user.exceptions import PasswordsDontMatch, UserAlreadyExists, UserDontExists, WrongPassword
from domain.services.user.models import LogInAnswer, LogInRequest, SignUpRequest
from postgre_module.repository.user_repository import UserRepository
from redis_module.models import SessionData
from redis_module.repository import RedisRepository
import uuid


class UserService():
    def __init__(self,
                 user_repository: UserRepository,
                 redis_repository: RedisRepository):
        self.user_repository = user_repository
        self.redis_repository = redis_repository

    async def signup(self, data: SignUpRequest):
        if data.password != data.repeat_password:
            raise PasswordsDontMatch
        username_checking = await self.user_repository.get_by_username(data.username)
        if username_checking is not None:
            raise UserAlreadyExists
        user = await self.user_repository.create(data.username, data.password)
        return user

    async def login(self, data: LogInRequest) -> LogInAnswer:
        user = await self.user_repository.get_by_username(data.username)
        if user is None:
            raise UserDontExists
        if not await self.user_repository.check_password(user, data.password):
            raise WrongPassword
        token = uuid.uuid4().hex
        await self.redis_repository.set_session_token(token,
                                                      SessionData(
                                                          user_id=user.id,
                                                          token=token)
                                                      )
        return LogInAnswer(token, user)

    async def logout(self, session_token: str):
        await self.redis_repository.remove_session_token(session_token)
