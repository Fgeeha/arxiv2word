FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev pandoc wget

ADD pyproject.toml /app

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем исходный код в контейнер
COPY src/ /app/src/

# Создаем папку для вывода
RUN mkdir -p /app/output

# Устанавливаем рабочий каталог и запускаем скрипт
CMD ["python", "/app/src/arxiv_to_word.py"]
