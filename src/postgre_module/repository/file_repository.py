from uuid import UUID
from postgre_module.models import File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> File | None:
        stmt = select(File).where(File.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def set_public_url(self, id: UUID, public_url: str):
        stmt = select(File).where(File.id == id).limit(1)
        file = await self.session.scalar(stmt)
        if file is None:
            return
        file.public_url = public_url

    async def create(self,
                     user_id: UUID,
                     s3_bucket: str,
                     s3_key: str,
                     file_name: str,
                     public_url: str | None = None,
                     flush=True) -> UUID:
        file = File(s3_bucket=s3_bucket,
                    s3_key=s3_key,
                    file_name=file_name,
                    public_url=public_url,
                    owner_id=user_id)
        self.session.add(file)
        if flush:
            await self.session.flush()
        return file.id