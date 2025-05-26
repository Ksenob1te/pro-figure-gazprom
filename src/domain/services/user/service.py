from domain.services.user.exceptions import PasswordsDontMatch, UserAlreadyExists, UserDontExists, UserRolesNotCreated, WrongPassword
from domain.services.user.models import LogInAnswer, LogInRequest, SignUpRequest
from postgre_module.repository.role_repository import RoleRepository
from postgre_module.repository.user_repository import UserRepository
from redis_module.models import SessionData
from redis_module.repository import RedisRepository
import uuid


class UserService():
    def __init__(self,
                 user_repository: UserRepository,
                 redis_repository: RedisRepository,
                 role_repository: RoleRepository):
        self.user_repository = user_repository
        self.redis_repository = redis_repository
        self.role_repository = role_repository

    async def signup(self, data: SignUpRequest):
        if data.password != data.repeat_password:
            raise PasswordsDontMatch
        username_checking = await self.user_repository.get_by_username(data.username)
        if username_checking is not None:
            raise UserAlreadyExists
        role = await self.role_repository.get_default()
        if role is None:
            raise UserRolesNotCreated
        await self.user_repository.create(data.username, data.password, role)

    async def login(self, data: LogInRequest) -> LogInAnswer:
        user = await self.user_repository.get_by_username(data.username)
        if user is None:
            raise UserDontExists
        if not await self.user_repository.check_password(user, data.password):
            raise WrongPassword
        token = uuid.uuid4().hex
        permissions = await self.role_repository.get_permissions(user.role)
        permissions = list(map(lambda x: x.name, permissions))

        await self.redis_repository.set_session_token(token,
                                                      SessionData(
                                                          user_id=user.id,
                                                          token=token,
                                                          permissions=permissions,
                                                          role=user.role.name,
                                                          user_name=user.username
                                                          )
                                                      )
        return LogInAnswer(token, user)

    async def logout(self, session_token: str):
        await self.redis_repository.remove_session_token(session_token)
