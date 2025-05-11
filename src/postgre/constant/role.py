from enum import Enum
from src.database import sessionmanager, Role, RoleRepository
import logging
from sqlalchemy.exc import IntegrityError


class RoleEnum(str, Enum):
    BLOCKED = 'blocked'
    GUEST = 'guest'
    ADMIN = 'admin'


async def create_roles():
    logger = logging.getLogger(__name__)
    async with sessionmanager.session() as session:
        role_repository = RoleRepository(session)
        for role in RoleEnum:
            try:
                await role_repository.create(role)
                logger.info(f"Role {role} created")
            except IntegrityError:
                await session.rollback()
                logger.info(f"Role {role} already exists")
        await session.commit()
