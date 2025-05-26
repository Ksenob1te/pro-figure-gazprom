from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class CourseData(BaseModel):
    class Config:
        orm_mode = True

    id: UUID
    title: str
    description: str
    category: str
    experience_level: str
    duration: int
    total_lessons: int
    created_date: datetime
    last_modified_date: datetime


class CourseFullData(BaseModel):
    class Config:
        orm_mode = True

    course: CourseData
    requirements: list[str]
    learn_points: list[str]


class UserCourseProgressData(BaseModel):
    class Config:
        orm_mode = True

    user_id: UUID
    course_id: UUID
    completed_lessons: int


class CourseListFullData(BaseModel):
    class Config:
        orm_mode = True

    courses: list[CourseFullData]

class CourseUserListData(BaseModel):
    class Config:
        orm_mode = True

    data: list[UserCourseProgressData]