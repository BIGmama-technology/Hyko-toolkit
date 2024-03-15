# Stage 1: Build stage for creating a venv with Poetry
FROM python:3.11.6-alpine as poetry-builder

# Set poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 

RUN pip install poetry

# Copy the project files
COPY pyproject.toml poetry.lock ./

# Cache poetry dependencies to speed up builds
RUN poetry install --without=dev,io --no-root --no-cache

# Stage 2: Application stage for running the application using the venv
FROM python:3.11.6-alpine as app-runner

RUN apk update

# Copy the virtual environment from the builder stage
COPY --from=poetry-builder /.venv /.venv
WORKDIR /app

# Activate the virtual environment
ENV VIRTUAL_ENV=/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
