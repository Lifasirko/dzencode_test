# Вибираємо базовий образ з Python
FROM python:3.12-slim

# Встановлюємо залежності
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Встановлення Poetry
RUN pip install poetry

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проекту в контейнер
COPY pyproject.toml poetry.lock ./

# Інсталяція залежностей через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Копіюємо весь код
COPY backend/ .

# Експортуємо порт для веб-сервісу
EXPOSE 8000

# Команда за замовчуванням
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
