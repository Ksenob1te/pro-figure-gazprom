from enum import Enum
import logging
from src.database import sessionmanager, PermissionRepository
from sqlalchemy.exc import IntegrityError


class PermissionsEnum(str, Enum):
    send_suggestions = 'send_suggestions'
    edit_materials = 'edit_materials'


async def create_permissions():
    logger = logging.getLogger(__name__)
    async with sessionmanager.session() as session:
        permission_repository = PermissionRepository(session)
        for permission in PermissionsEnum:
            try:
                await permission_repository.create(permission)
                logger.info(f"Permission {permission} created")
            except IntegrityError:
                await session.rollback()
                logger.info(f"Permission {permission} already exists")
        await session.commit()
