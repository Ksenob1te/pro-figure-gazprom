import asyncio
from types import CoroutineType
from postgre_module.engine import get_db_session, sessionmanager
from postgre_module.repository.achievement_repository import AchievementRepository
from postgre_module.repository.permission_repository import PermissionRepository
from postgre_module.repository.role_repository import RoleRepository


async def create_achievements():
    async with sessionmanager.session() as session:
        achievement_repositpry = AchievementRepository(session)

        futures = []
        futures.append(achievement_repositpry.create(
            code="real_programmer",
            name="Real programmer",
            description="4/5 Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="perfectionist",
            name="Perfectionist",
            description="1/5 Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="lead_the_world",
            name="Lead the World",
            description="3/5 Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="welcome_essential_plus",
            name="Welcome on Essential+",
            description="No Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="good_buddy",
            name="Good buddy",
            description="4/5 Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="real_veteran",
            name="Real veteran",
            description="No Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="mentor_hackathon",
            name="Mentor at the hackathon",
            description="5/5 Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repositpry.create(
            code="top5_hackchange2024",
            name="Top 5% Hack Change 2024",
            description="No Rank",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        await asyncio.gather(*futures)