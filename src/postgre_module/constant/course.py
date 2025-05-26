import asyncio
from uuid import uuid4
from postgre_module.engine import sessionmanager
from postgre_module.repository.course_repository import CourseRepository


async def create_courses():
    async with sessionmanager.session() as session:
        repository = CourseRepository(session)
        futures = []

        courses_data = [
            {
                "title": "Основы машинного обучения",
                "description": "Изучите основы ML, включая классические алгоритмы и современные подходы.",
                "category": "ai",
                "experience_level": "Без опыта",
                "duration": 48,
                "total_lessons": 24,
                "requirements": ["Базовые знания Python", "Основы математики"],
                "learn_points": [
                    "Основные алгоритмы ML",
                    "Работа с данными",
                    "Построение моделей"
                ]
            },
            {
                "title": "Разработка Web-приложений на React",
                "description": "Создавайте современные веб-приложения с использованием React, Redux и современных инструментов разработки.",
                "category": "dev",
                "experience_level": "С опытом",
                "duration": 56,
                "total_lessons": 32,
                "requirements": ["JavaScript", "HTML/CSS", "Базовые знания веб-разработки"],
                "learn_points": [
                    "React и его экосистема",
                    "Управление состоянием",
                    "Оптимизация производительности"
                ]
            },
            {
                "title": "Современные технологии DevOps",
                "description": "Погрузитесь в мир DevOps: контейнеризация, CI/CD, облачные сервисы и автоматизация.",
                "category": "tech",
                "experience_level": "С опытом",
                "duration": 42,
                "total_lessons": 28,
                "requirements": ["Linux", "Базовые знания сетей", "Git"],
                "learn_points": [
                    "Docker и Kubernetes",
                    "CI/CD пайплайны",
                    "Мониторинг и логирование"
                ]
            },
            {
                "title": "Управление IT-проектами",
                "description": "Освойте ключевые навыки управления IT-проектами, от планирования до успешного запуска.",
                "category": "business",
                "experience_level": "Без опыта",
                "duration": 36,
                "total_lessons": 20,
                "requirements": ["Базовые знания IT", "Английский язык"],
                "learn_points": [
                    "Agile методологии",
                    "Управление командой",
                    "Оценка рисков"
                ]
            },
            {
                "title": "Нейронные сети и Deep Learning",
                "description": "Изучите глубокое обучение, архитектуры нейронных сетей и их применение в реальных проектах.",
                "category": "ai",
                "experience_level": "С опытом",
                "duration": 64,
                "total_lessons": 40,
                "requirements": ["Python", "Математическая статистика", "ML основы"],
                "learn_points": [
                    "CNN и RNN архитектуры",
                    "Transfer Learning",
                    "Развертывание моделей"
                ]
            },
        ]

        for course in courses_data:
            course_id = uuid4()
            futures.append(repository.create(
                id=course_id,
                title=course["title"],
                description=course["description"],
                category=course["category"],
                experience_level=course["experience_level"],
                duration=course["duration"],
                total_lessons=course["total_lessons"],
                flush=False
            ))

            for requirement in course["requirements"]:
                futures.append(repository.add_requirement(course_id, requirement, flush=False))

            for point in course["learn_points"]:
                futures.append(repository.add_learning_point(course_id, point, flush=False))

        await asyncio.gather(*futures)

# Запуск
if __name__ == "__main__":
    asyncio.run(create_courses())
