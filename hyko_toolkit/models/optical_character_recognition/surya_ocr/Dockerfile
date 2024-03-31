FROM hykoai/hyko-sdk-medium:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install surya-ocr
RUN --mount=type=cache,target=/root/.cache/pip pip install torch
COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
