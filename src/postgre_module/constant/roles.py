import asyncio
from types import CoroutineType
from postgre_module.engine import get_db_session, sessionmanager
from postgre_module.repository.permission_repository import PermissionRepository
from postgre_module.repository.role_repository import RoleRepository


async def create_roles():
    session_context = get_db_session()
    session = await session_context.__anext__()
    role_repository = RoleRepository(session)
    permission_repository = PermissionRepository(session)

    to_create: list[CoroutineType] = []

    to_create.append(role_repository.create("Administrator", False))
    to_create.append(role_repository.create("User", False))

    await asyncio.gather(*to_create)

    to_create: list[CoroutineType] = []

    await asyncio.gather(*to_create)
    try:
        await session_context.__anext__()
    except:
        pass