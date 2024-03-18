FROM hyko-sdk:latest

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip pip install langchain 
RUN --mount=type=cache,target=/root/.cache/pip pip install sentence_transformers
RUN --mount=type=cache,target=/root/.cache/pip pip install faiss-cpu
RUN --mount=type=cache,target=/root/.cache/pip pip install rank_bm25
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
