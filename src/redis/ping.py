import redis.asyncio as redis
import asyncio


async def main():
    pool = redis.ConnectionPool.from_url("redis://default:redisPassword@localhost")
    client = redis.Redis.from_pool(pool)
    await client.ping()
    await client.aclose()
    await pool.aclose()


if __name__ == "__main__":
    asyncio.run(main())

