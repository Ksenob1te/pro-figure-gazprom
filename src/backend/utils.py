
from typing import Annotated

from redis_module.models import SessionData
from redis_module.repository import RedisRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Request
from postgre_module.engine import get_db_session
from redis.asyncio import Redis
from redis_module.service import get_redis_client



GetRedisClient = Annotated[Redis, Depends(get_redis_client)]
GetDBSession = Annotated[AsyncSession, Depends(get_db_session)]

async def get_user_optional(request: Request, redis: GetRedisClient) -> SessionData | None:
    redis_repository = RedisRepository(redis)
    token = request.cookies.get("token")
    if token is None:
        return None
    session_data = await redis_repository.get_by_session_token(token)
    return session_data

GetOptionalUser = Annotated[SessionData | None, Depends(get_user_optional)]

async def get_user(user: GetOptionalUser) -> SessionData:
    if user is None:
        raise HTTPException(401, "Not authenticated")
    return user

GetUser = Annotated[SessionData, get_user]