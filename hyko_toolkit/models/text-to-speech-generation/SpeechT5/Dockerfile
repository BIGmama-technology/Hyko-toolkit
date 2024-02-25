FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install transformers[torch]
RUN --mount=type=cache,target=/root/.cache/pip pip install accelerate
RUN --mount=type=cache,target=/root/.cache/pip pip install sentencepiece
RUN --mount=type=cache,target=/root/.cache/pip pip install einops 
RUN --mount=type=cache,target=/root/.cache/pip pip install datasets

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
