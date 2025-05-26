from uuid import UUID
from src.postgre_module import CourseRepository, UserCourseRepository
from .models import CourseCreateRequest, CourseRequirementRequest, CourseLearnRequest
from .exceptions import CourseNotFound, UserAlreadyEnrolled
from postgre_module.models import Course, CourseRequirement, CourseLearn, UserCourse


class CourseService:
    def __init__(
        self,
        course_repository: CourseRepository,
        user_course_repository: UserCourseRepository
    ):
        self.course_repository = course_repository
        self.user_course_repository = user_course_repository

    async def get_course_by_id(self, course_id: UUID) -> Course:
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            raise CourseNotFound(f"Course with id {course_id} not found")
        return course

    async def get_all(self) -> list[Course]:
        return await self.course_repository.get_all()

    async def create_course(self, data: CourseCreateRequest) -> Course:
        course = await self.course_repository.create(**data.__dict__)
        return course

    async def add_course_requirement(self, data: CourseRequirementRequest) -> None:
        await self.course_repository.add_requirement(
            course_id=data.course_id, requirement=data.requirement
        )

    async def add_course_learning_point(self, data: CourseLearnRequest) -> None:
        await self.course_repository.add_learning_point(
            course_id=data.course_id, learn=data.learn
        )

    async def get_course_requirements(self, course_id: UUID) -> list[CourseRequirement]:
        return await self.course_repository.get_requirements(course_id)

    async def get_course_requirements_str(self, course_id: UUID) -> list[str]:
        array = await self.course_repository.get_requirements(course_id)
        return [req.requirements for req in array]

    async def get_course_learning_points(self, course_id: UUID) -> list[CourseLearn]:
        return await self.course_repository.get_learning_points(course_id)

    async def get_course_learning_points_str(self, course_id: UUID) -> list[str]:
        array = await self.course_repository.get_learning_points(course_id)
        return [point.learn for point in array]

    async def enroll_user_to_course(self, user_id: UUID, course_id: UUID) -> UserCourse:
        existing = await self.user_course_repository.get_by_user_and_course(user_id, course_id)
        if existing:
            raise UserAlreadyEnrolled(f"User already enrolled in course {course_id}")

        return await self.user_course_repository.enroll_user(user_id, course_id)

    async def update_course_progress(self, user_id: UUID, course_id: UUID, completed_lessons: int) -> bool:
        return await self.user_course_repository.update_progress(user_id, course_id, completed_lessons)

    async def get_user_courses(self, user_id: UUID) -> list[UserCourse]:
        return await self.user_course_repository.get_user_courses(user_id)
