class DomainException(Exception):
    http_code: int | None
    http_message: str | None