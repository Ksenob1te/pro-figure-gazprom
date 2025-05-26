from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from postgre_module.models import UserCourse


class UserCourseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def enroll_user(self, user_id: UUID, course_id: UUID) -> UserCourse:
        user_course = UserCourse(user_id=user_id, course_id=course_id)
        self.session.add(user_course)
        await self.session.flush()
        return user_course

    async def get_user_courses(self, user_id: UUID) -> list[UserCourse]:
        stmt = select(UserCourse).where(UserCourse.user_id == user_id)
        result = await self.session.scalars(stmt)
        return list(result)

    async def get_by_user_and_course(self, user_id: UUID, course_id: UUID) -> UserCourse | None:
        stmt = select(UserCourse).where(
            and_(UserCourse.user_id == user_id, UserCourse.course_id == course_id)
        )
        return await self.session.scalar(stmt)

    async def update_progress(self, user_id: UUID, course_id: UUID, completed_lessons: int) -> bool:
        user_course = await self.get_by_user_and_course(user_id, course_id)
        if not user_course:
            return False
        user_course.completed_lessons = completed_lessons
        await self.session.flush()
        return True

    async def get_completed_courses(self, user_id: UUID) -> list[UserCourse]:
        stmt = select(UserCourse).where(
            and_(
                UserCourse.user_id == user_id,
                UserCourse.completed_lessons >= UserCourse.course.total_lessons
            )
        )
        result = await self.session.scalars(stmt)
        return list(result)
