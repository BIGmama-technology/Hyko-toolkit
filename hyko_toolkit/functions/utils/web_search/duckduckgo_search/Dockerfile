FROM base:latest as deps

RUN --mount=type=cache,target=/root/.cache/pip pip install duckduckgo_search

FROM hyko-sdk:latest
COPY --from=deps /.venv /.venv

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "--loop" , "asyncio", "main:func"]
