from . import *
import asyncio

async def init_constants():
    # await create_permissions()
    await create_roles()
    await create_achievements()
    await create_courses()
    # await create_role_permission()
    # await create_texts()
    pass

if __name__ == "__main__":
    asyncio.run(init_constants())