from domain.base_exception import DomainException


class UserAlreadyExists(DomainException):
    pass

class WrongPassword(DomainException):
    pass

class PasswordsDontMatch(DomainException):
    pass

class UserDontExists(DomainException):
    pass