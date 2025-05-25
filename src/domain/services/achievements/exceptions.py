from domain.base_exception import DomainException


class AchievementAlreadyEarned(DomainException):
    pass

class AchievementNotFound(DomainException):
    pass

class UserStatsNotFound(DomainException):
    pass

class UserStatsAlreadyExists(DomainException):
    pass

class AchievementAlreadyExists(DomainException):
    pass

