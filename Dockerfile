FROM python:3.12-alpine3.19
LABEL authors="Bogdan"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


RUN apk update && \
    apk add --no-cache postgresql-client gcc musl-dev


RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /app/


RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

RUN addgroup appgroup && adduser -S -G appuser

USER appuser


ENTRYPOINT ["python", "manage.py", "runserver"]
