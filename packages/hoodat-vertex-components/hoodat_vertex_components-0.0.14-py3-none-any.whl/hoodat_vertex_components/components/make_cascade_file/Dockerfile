FROM python:3.9-alpine

RUN pip install poetry

COPY pyproject.toml .

RUN poetry install --no-dev

COPY . .
