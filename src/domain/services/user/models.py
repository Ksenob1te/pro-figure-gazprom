from dataclasses import dataclass
from postgre_module.models import User


@dataclass
class SignUpRequest():
    username: str
    password: str
    repeat_password: str


@dataclass
class LogInRequest():
    username: str
    password: str


@dataclass
class LogInAnswer():
    token: str
    user: User
