FROM base:latest as deps

RUN --mount=type=cache,target=/root/.cache/pip pip install playwright 
RUN --mount=type=cache,target=/root/.cache/pip pip install langchain
RUN --mount=type=cache,target=/root/.cache/pip pip install beautifulsoup4 
RUN --mount=type=cache,target=/root/.cache/pip pip install nest_asyncio

FROM hyko-sdk:latest
COPY --from=deps /.venv /.venv

RUN apt-get update && \
    apt-get install -y curl sudo xvfb libatk-bridge2.0-0 libgtk-3-0 libnss3 libx11-xcb1 libxcb-dri3-0 libdrm2 libxshmfence1 libgbm1 && \
    apt-get install -y --no-install-recommends nodejs npm && \
    npm install -g playwright && \
    export PATH="$PATH:$(npm bin)"
RUN playwright install chromium

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "--loop", "asyncio", "main:func"]
