from domain.base_exception import DomainException


class CourseNotFound(DomainException):
    pass


class UserAlreadyEnrolled(DomainException):
    pass
