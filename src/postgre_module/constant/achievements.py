import asyncio
from types import CoroutineType
from postgre_module.engine import get_db_session, sessionmanager
from postgre_module.repository.achievement_repository import AchievementRepository
from postgre_module.repository.permission_repository import PermissionRepository
from postgre_module.repository.role_repository import RoleRepository


async def create_achievements():
    async with sessionmanager.session() as session:
        achievement_repository = AchievementRepository(session)

        futures = []
        futures.append(achievement_repository.create(
            code="real_programmer",
            name="Real programmer",
            description="Задача: успешно выполнить 15 проектов.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="perfectionist",
            name="Perfectionist",
            description="Задача: успешно выполнить 5 проектов подряд.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="lead_the_world",
            name="Lead the World",
            description="Задача: лидировать 7 групповых проектов.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="welcome_essential_plus",
            name="Welcome on Essential+",
            description="Задача: успешно поступить на курс уровня Essential+.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="good_buddy",
            name="Good buddy",
            description="Задача: помочь в адаптации студентам, уровня ниже Essential+.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="real_veteran",
            name="Real veteran",
            description="Задача: проведи с нами первый свой День рождения!",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="mentor_hackathon",
            name="Mentor at the hackathon",
            description="Задача: ментор на хакатоне более 15 раз.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        futures.append(achievement_repository.create(
            code="top5_hackchange2024",
            name="Top 5% Hack Change 2024",
            description="Задача: победа на хакатоне Hack Change от Газпром Нефти.",
            experience_reward=100,
            is_hidden=False,
            flush=False
        ))

        await asyncio.gather(*futures)