FROM base:latest

# Set poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 

RUN pip install poetry

# Copy the project files
COPY pyproject.toml poetry.lock ./

# Cache poetry dependencies to speed up builds
RUN poetry install --without dev --no-root --no-cache

# Copy the application code
WORKDIR /hyko_sdk
COPY hyko_sdk .

# Install project dependencies excluding the dev dependencies
RUN poetry install --without dev --no-cache

WORKDIR /app