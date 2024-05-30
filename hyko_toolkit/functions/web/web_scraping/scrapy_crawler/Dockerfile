FROM hykoai/toolkit-base:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install BeautifulSoup4
RUN --mount=type=cache,target=/root/.cache/pip pip install bs4
RUN --mount=type=cache,target=/root/.cache/pip pip install scrapy
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
