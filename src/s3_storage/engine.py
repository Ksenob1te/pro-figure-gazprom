from minio import Minio
from settings.env_config import Settings

async def get_s3_client() -> Minio:
    return Minio(
        endpoint=f"{Settings.s3.ip}:{Settings.s3.port}",
        access_key=Settings.s3.access_key,
        secret_key=Settings.s3.secret_key,
        secure=Settings.s3.secure
    )