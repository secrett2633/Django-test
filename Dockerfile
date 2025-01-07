FROM python:3.10.11 AS builder

ARG POETRY_VERSION=1.5.1

RUN python -m pip install --no-cache-dir poetry==${POETRY_VERSION}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workdir

COPY pyproject.toml poetry.lock /workdir/
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY dockerize.tar.gz /tmp/
RUN tar -C /usr/local/bin -xzvf /tmp/dockerize.tar.gz
COPY .env gunicorn.conf.py manage.py /workdir/
COPY /app /workdir/app