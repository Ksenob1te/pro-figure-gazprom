from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import UserReminder
from uuid import UUID
import logging


# UserReminder(user_id: UUID, notification_times: List[int])
class UserReminderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_by_user_id(self, user_id: UUID) -> UserReminder | None:
        stmt = select(UserReminder).where(UserReminder.user_id == user_id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user_id: UUID, notification_times: list[int]) -> UserReminder:
        user_reminder = UserReminder(user_id=user_id, notification_times=notification_times)
        self.session.add(user_reminder)
        await self.session.flush()
        return user_reminder

    async def add_notification_time(self, user_reminder: UserReminder, notification_time: int) -> UserReminder:
        user_reminder.notification_times.append(notification_time)
        await self.session.flush()
        return user_reminder

    async def set_notification_times(self, user_reminder: UserReminder, notification_times: list[int]) -> UserReminder:
        user_reminder.notification_times = notification_times
        await self.session.flush()
        return user_reminder
