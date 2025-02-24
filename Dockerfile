FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Копирование pyproject.toml
COPY pyproject.toml /app

# Обновление пакетов, установка зависимостей
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-dev pandoc wget && \
    apt-get clean && \
     rm -rf /var/lib/apt/lists/* &&\
    pip install --upgrade --no-cache-dir  pip  && \
    pip install --no-cache-dir  poetry  && \
    poetry completions bash >> ~/.bash_completion && \
    poetry lock --no-update && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем исходный код
COPY src/ /app/src/

# Создаем папку для вывода
RUN mkdir -p /app/output

# Запуск приложения
CMD ["poetry","run","python", "/app/src/arxiv_to_word.py"]
