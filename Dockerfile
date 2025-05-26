# Базовый образ Python (указана версия >= 3.13)
FROM python:3.13-rc-bookworm

# Установка poetry или pip зависимости — тут pip, так как astra-uv не требует poetry
# Обновим pip, setuptools и wheel
RUN pip install --upgrade pip setuptools wheel

# Создаем рабочую директорию
WORKDIR /app

# Копируем pyproject.toml и README.md (если есть)
COPY pyproject.toml README.md ./

# Устанавливаем зависимости через astra-uv
RUN pip install astra-uv && uv pip install --system .

# Копируем исходный код
COPY src/ ./src/

# Пробрасываем переменные (опционально)
ENV PYTHONUNBUFFERED=1

# Команда запуска приложения
CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "80"]