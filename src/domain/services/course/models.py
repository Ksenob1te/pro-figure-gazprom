from uuid import UUID
from dataclasses import dataclass


@dataclass
class CourseCreateRequest:
    title: str
    description: str
    category: str
    experience_level: str
    duration: int
    total_lessons: int


@dataclass
class CourseRequirementRequest:
    course_id: UUID
    requirement: str


@dataclass
class CourseLearnRequest:
    course_id: UUID
    learn: str
