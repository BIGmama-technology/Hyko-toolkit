FROM hyko-sdk-tiny:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install scikit_learn

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
