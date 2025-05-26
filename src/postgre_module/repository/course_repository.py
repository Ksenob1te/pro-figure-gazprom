from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from postgre_module.models import Course, CourseRequirement, CourseLearn


class CourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, course_id: UUID) -> Course | None:
        stmt = select(Course).where(Course.id == course_id)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Course]:
        stmt = select(Course)
        result = await self.session.scalars(stmt)
        return list(result)

    async def create(self, **kwargs) -> Course:
        flush = kwargs.pop('flush')
        course = Course(**kwargs)
        self.session.add(course)
        if flush:
            await self.session.flush()
        return course

    async def add_requirement(self, course_id: UUID, requirement: str, flush=True) -> None:
        requirement_entry = CourseRequirement(course_id=course_id, requirements=requirement)
        self.session.add(requirement_entry)
        if flush:
            await self.session.flush()

    async def add_learning_point(self, course_id: UUID, learn: str, flush=True) -> None:
        learning_entry = CourseLearn(course_id=course_id, learn=learn)
        self.session.add(learning_entry)
        if flush:
            await self.session.flush()

    async def get_requirements(self, course_id: UUID) -> list[CourseRequirement]:
        stmt = select(CourseRequirement).where(CourseRequirement.course_id == course_id)
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_learning_points(self, course_id: UUID) -> list[CourseLearn]:
        stmt = select(CourseLearn).where(CourseLearn.course_id == course_id)
        result = await self.session.scalars(stmt)
        return list(result)

