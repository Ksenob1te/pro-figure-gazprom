from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class PostgresConfig(BaseModel):
    host: str = "localhost"
    port: int = 25432
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

class S3Config(BaseModel):
    ip: str = "minio"
    port: int = 9000
    access_key: str = "MINIO_ACCESS_KEY"
    secret_key: str = "MINIO_SECRET_KEY"
    user: str = "minioadmin"
    password: str = "minioadmin"
    bucket: str = "my-bucket"
    secure: bool = False

class TTLConfig(BaseModel):
    auth_token_expire: int = 60*60*24*30

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=['.env.prod', '.env.local', '.env'], env_nested_delimiter="_")

    postgres: PostgresConfig = PostgresConfig()
    redis: RedisConfig = RedisConfig()
    s3: S3Config = S3Config()
    ttl: TTLConfig = TTLConfig()


APP_SETTINGS = Settings()