from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    name: str = "pro-figure"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    user: str = "default"
    password: str = "redis"

class TTLConfig(BaseModel):
    auth_token_expire: int = 60*60*24*30

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter="_")

    postgres: PostgresConfig = PostgresConfig()
    redis: RedisConfig = RedisConfig()
    ttl: TTLConfig = TTLConfig()


APP_SETTINGS = Settings()