FROM hyko-sdk-medium:latest

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip pip install langchain 
RUN --mount=type=cache,target=/root/.cache/pip pip install sentence_transformers
RUN --mount=type=cache,target=/root/.cache/pip pip install faiss-cpu
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
