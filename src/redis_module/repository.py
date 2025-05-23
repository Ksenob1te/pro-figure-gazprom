import json
from settings.env_config import APP_SETTINGS
from redis.asyncio import Redis
from redis_module.models import SessionData


class RedisRepository():
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_by_session_token(self, session_id: str) -> SessionData | None:
        response: str = await self.redis.get("auth:"+session_id)
        if response is None:
            return None
        return SessionData.model_validate_json(response)

    async def set_session_token(self, session_id: str, session_data: SessionData):
        await self.redis.set("auth:"+session_id,
                             session_data.model_dump_json(),
                             ex=APP_SETTINGS.ttl.auth_token_expire)

    async def remove_session_token(self, session_id: str):
        await self.redis.delete("auth:"+session_id)
