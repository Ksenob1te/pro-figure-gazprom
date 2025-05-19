from redis.asyncio import Redis, ConnectionPool
from settings import APP_SETTINGS

REDIS_POOL = None


def build_redis_string(username: str,
                       password: str,
                       address: str,
                       port: int,
                       db: str = "0",
                       ssl=False):
    return f"redis{'s' if ssl else ''}://{username}:{password}@{address}:{port}/{db}"


async def setup_redis_pool():
    global REDIS_POOL
    REDIS_POOL = ConnectionPool.from_url(build_redis_string(APP_SETTINGS.redis.user,
                                                            APP_SETTINGS.redis.password,
                                                            APP_SETTINGS.redis.host,
                                                            APP_SETTINGS.redis.port))


async def free_redis_pool():
    if REDIS_POOL is None:
        return
    await REDIS_POOL.aclose()


async def get_redis_client():
    if REDIS_POOL is None:
        raise Exception("Redis pool not initialized")
    client = Redis(connection_pool=REDIS_POOL)
    yield client
    await client.aclose()
