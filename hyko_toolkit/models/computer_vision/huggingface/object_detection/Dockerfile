FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install torch
RUN --mount=type=cache,target=/root/.cache/pip pip install transformers
RUN --mount=type=cache,target=/root/.cache/pip pip install accelerate
RUN --mount=type=cache,target=/root/.cache/pip pip install timm
RUN --mount=type=cache,target=/root/.cache/pip pip install opencv-python

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
