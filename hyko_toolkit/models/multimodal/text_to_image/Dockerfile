FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install transformers[torch]
RUN --mount=type=cache,target=/root/.cache/pip pip install diffusers[torch]

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
