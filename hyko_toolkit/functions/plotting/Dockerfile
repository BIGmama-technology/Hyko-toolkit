FROM hykoai/hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install matplotlib pandas seaborn

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
