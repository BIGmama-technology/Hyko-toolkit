FROM hykoai/toolkit-base:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install opencv-python
RUN --mount=type=cache,target=/root/.cache/pip pip install torch
RUN --mount=type=cache,target=/root/.cache/pip pip install torchvision
RUN --mount=type=cache,target=/root/.cache/pip pip install supervision
RUN --mount=type=cache,target=/root/.cache/pip pip install ultralytics
RUN --mount=type=cache,target=/root/.cache/pip pip install cvzone
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
