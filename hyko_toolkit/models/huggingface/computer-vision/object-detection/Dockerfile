FROM hyko-sdk:latest

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip pip install timm opencv-python

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000","main:func"]
