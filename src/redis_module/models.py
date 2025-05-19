from uuid import UUID

from pydantic import BaseModel

class SessionData(BaseModel):
    user_id: UUID
    token: str