from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

class PostgresConfig(BaseModel):
    host: str = Field(default="localhost", alias="POSTGRES_HOST")
    port: int = Field(default=5432, alias="POSTGRES_PORT")
    user: str = Field(default="postgres", alias="POSTGRES_USER")
    password: str = Field(default="postgres", alias="POSTGRES_PASSWORD")
    name: str = Field(default="redditrot", alias="POSTGRES_NAME")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str = Field(default="localhost", alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")
    user: str = Field(default="default", alias="REDIS_USER")
    password: str = Field(default="redis", alias="REDIS_PASSWORD")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env.prod', '.env.local'), extra="ignore")

    postgres: PostgresConfig = PostgresConfig()
    redis: RedisConfig = RedisConfig()


env = Settings()
