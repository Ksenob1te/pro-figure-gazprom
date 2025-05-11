import logging
from src.database import sessionmanager, RoleRepository, PermissionRepository
from . import RoleEnum, PermissionsEnum


async def create_role_permission():
    logger = logging.getLogger(__name__)
    async with sessionmanager.session() as session:
        role_repository = RoleRepository(session)
        permission_repository = PermissionRepository(session)
        admin_role = await role_repository.get_by_name(RoleEnum.ADMIN.value)
        send_suggestions = await permission_repository.get_by_name(PermissionsEnum.send_suggestions)
        edit_materials = await permission_repository.get_by_name(PermissionsEnum.edit_materials)
        await role_repository.add_permission(role=admin_role, permission=send_suggestions)
        await role_repository.add_permission(role=admin_role, permission=edit_materials)
        logger.info(f"Permissions for admin granted")

        guest_role = await role_repository.get_by_name(RoleEnum.GUEST.value)
        await role_repository.add_permission(role=guest_role, permission=send_suggestions)
        logger.info(f"Permissions for guest granted")
        await session.commit()