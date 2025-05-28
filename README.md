# Pro Figure Gazprom

**Pro Figure Gazprom** — образовательная платформа, построенная на FastAPI с использованием PostgreSQL, Redis, MinIO и асинхронного подхода. Проект реализован с разделением по слоям: API, домены, хранилище и инфраструктура.

---

## Основные возможности

- Работа с файлами через S3-хранилище (MinIO)
- Кэширование и фоновые операции через Redis
- Асинхронные репозитории с SQLAlchemy
- Поддержка Docker и локальной разработки через `uv`

---

---

## Быстрый старт (локально через uv)

### Установка `uv`

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

### Инициализация проекта
```bash
uv init --python 3.10
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Применение миграций
С помощью скрипта:
```bash
bash src/postgre_module/migrate.bat
```
Или с вручную:
```bash
cd src/postgre_module
alembic upgrade head
```

### Запуск проекта
```bash
bash start.bat
```
Или вручную:
```bash
uvicorn src.backend.app:app --reload
```

После запуска приложение будет доступно по адресу:
http://localhost:8000/api/docs

## Быстрый старт (Docker)
### Сборка и запуск контейнера
```bash
docker-compose up --build
```

## Конфигурация
Конфигурация проекта осуществляется через файл `config.toml` и переменные окружения. Основные параметры:

Пример .env
```env
# PostgreSQL Database Configuration
postgres_host=localhost
postgres_port=25432
postgres_user=postgres
postgres_password=postgres
postgres_name=pro-figure

# Redis Configuration
redis_host=localhost
redis_port=6379
redis_user=default
redis_password=redis

# MinIO / S3 Configuration
s3_ip=minio
s3_port=9000
s3_access_key=MINIO_ACCESS_KEY
s3_secret_key=MINIO_SECRET_KEY
s3_user=minioadmin
s3_password=minioadmin
s3_bucket=my-bucket
s3_secure=False

# Token TTL Configuration (in seconds)
ttl_auth_token_expire=2592000  # 30 days
```

