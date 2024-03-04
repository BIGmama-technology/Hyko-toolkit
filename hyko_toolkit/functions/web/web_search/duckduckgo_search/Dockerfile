FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install duckduckgo_search

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "--loop" , "asyncio", "main:func"]
