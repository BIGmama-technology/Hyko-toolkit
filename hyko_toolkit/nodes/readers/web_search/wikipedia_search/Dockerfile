FROM hykoai/toolkit-base:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install wikipedia

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
