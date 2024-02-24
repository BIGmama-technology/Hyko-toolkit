FROM base:latest as deps

RUN --mount=type=cache,target=/root/.cache/pip pip install langchain 
RUN --mount=type=cache,target=/root/.cache/pip pip install sentence_transformers
RUN --mount=type=cache,target=/root/.cache/pip pip install faiss-cpu

FROM hyko-sdk:latest
COPY --from=deps /.venv /.venv

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
