FROM base:latest as deps

RUN apt update && apt install -y git
RUN --mount=type=cache,target=/root/.cache/pip pip install transformers[torch]
RUN --mount=type=cache,target=/root/.cache/pip pip install accelerate
RUN --mount=type=cache,target=/root/.cache/pip pip install "git+https://github.com/suno-ai/bark.git"

FROM hyko-sdk:latest
COPY --from=deps /.venv /.venv

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
