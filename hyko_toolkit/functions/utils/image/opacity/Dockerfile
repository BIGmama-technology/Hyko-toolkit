FROM hyko-sdk:latest

RUN --mount=type=cache,target=/root/.cache/pip pip install opencv-python==4.8.0.76 

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
