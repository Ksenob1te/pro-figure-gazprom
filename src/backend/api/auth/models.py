from uuid import UUID
from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: UUID
    permissions: list[str]
    role: str

class SignUpRequest(BaseModel):
    username: str
    password: str
    repeat_password: str

class LogInRequest(BaseModel):
    username: str
    password: str
    