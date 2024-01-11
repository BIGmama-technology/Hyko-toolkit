FROM python:3.11.6-slim

RUN apt update && \
    apt install -y --no-install-recommends build-essential libgl1-mesa-glx libglib2.0-0 ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

WORKDIR /hyko_sdk
COPY hyko_sdk .
RUN poetry install --without dev
