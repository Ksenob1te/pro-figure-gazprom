from backend.dependencies import CourseServiceDepends
from .models import *
from backend.utils import GetUser
from fastapi_controllers import Controller, get, post


class CourseController(Controller):
    prefix = "/courses"
    tags = ["courses"]

    def __init__(self, course_service: CourseServiceDepends):
        super().__init__()
        self.course_service = course_service

    @get("/", response_model=CourseListFullData)
    async def get_all_courses(self):
        courses = await self.course_service.get_all()
        result = []
        for course in courses:
            requirements = await self.course_service.get_course_requirements_str(course.id)
            learn_points = await self.course_service.get_course_learning_points_str(course.id)

            result.append(
                {
                    "course": course,
                    "requirements": requirements,
                    "learn_points": learn_points
                }
            )
        return {"courses": result}

    @get("/user", response_model=CourseUserListData)
    async def get_user_courses(self, user: GetUser):
        user_courses = await self.course_service.get_user_courses(user.user_id)
        return {"data": user_courses}

    @post("/enroll", response_model=UserCourseProgressData)
    async def enroll_user_to_course(self, user: GetUser, course_id: UUID):
        user_course = await self.course_service.enroll_user_to_course(user.user_id, course_id)
        return UserCourseProgressData(
            user_id=user.user_id,
            course_id=course_id,
            completed_lessons=user_course.completed_lessons
        )
