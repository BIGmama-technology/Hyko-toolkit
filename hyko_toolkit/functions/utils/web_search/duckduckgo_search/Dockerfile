FROM hyko-sdk:latest

RUN pip install --no-cache-dir duckduckgo_search

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "--loop" , "asyncio", "main:func"]
