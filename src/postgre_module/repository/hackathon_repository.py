from uuid import UUID
from postgre_module.models import File, Hackathon, HackathonDirection, HackathonFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HackathonRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID):
        stmt = select(Hackathon).where(Hackathon.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self, limit: int = 10, offset: int = 0):
        stmt = select(Hackathon).limit(limit).offset(offset)
        return list((await self.session.scalars(stmt)).all())

    async def add_file(self, hackathon: Hackathon, file: File):
        hackathon_file = HackathonFile(
            hackathon_id=hackathon.id, file_id=file.id)
        self.session.add(hackathon_file)

    async def remove_file(self, hackathon: Hackathon, file: File):
        stmt = select(HackathonFile).where(HackathonFile.hackathon_id ==
                                           hackathon.id).where(HackathonFile.file_id == file.id).limit(1)
        hackathon_file = await self.session.scalar(stmt)
        if hackathon_file is None:
            return
        await self.session.delete(hackathon_file)

    async def get_files(self, hackathon: Hackathon):
        stmt = select(HackathonFile).where(
            HackathonFile.hackathon_id == hackathon.id)
        return list((await self.session.scalars(stmt)).all())

    async def create(self,
                     name: str,
                     description: str,
                     max_team_size: int,
                     max_solution_count: int,
                     start_registration: str,
                     end_registration: str,
                     start_date: str,
                     end_date: str,
                     directions: HackathonDirection,
                     flush=True):
        hackathon = Hackathon(name=name,
                              description=description,
                              start_date=start_date,
                              end_date=end_date,
                              direction_id=directions.id,
                              max_team_size=max_team_size,
                              max_solution_count=max_solution_count,
                              start_registration=start_registration,
                              end_registration=end_registration)
        self.session.add(hackathon)
        if flush:
            await self.session.flush()
