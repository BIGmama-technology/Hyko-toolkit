FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install ultralytics
RUN --mount=type=cache,target=/root/.cache/pip pip install cvzone
RUN --mount=type=cache,target=/root/.cache/pip pip install opencv-python
RUN --mount=type=cache,target=/root/.cache/pip pip install supervision
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
