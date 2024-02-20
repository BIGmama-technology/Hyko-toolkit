FROM python:3.11.6-slim

RUN apt update && \
    apt install -y --no-install-recommends build-essential libgl1-mesa-glx libglib2.0-0 ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=~/.cache/pypoetry/cache \
    --mount=type=cache,target=~/.cache/pypoetry/artifacts

RUN poetry install --without dev --no-root --no-cache

# Conditional installation based on the build argument
ARG INSTALL_OPTIONAL_PACKAGES=false
RUN if [ "$INSTALL_OPTIONAL_PACKAGES" = "true" ] ; then poetry add --no-cache transformers[torch] diffusers[torch] accelerate sentencepiece; fi

WORKDIR /hyko_sdk
COPY hyko_sdk .
RUN poetry install --without dev --no-cache
