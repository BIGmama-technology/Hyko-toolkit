FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry run pip install --no-cache-dir opencv-python==4.8.0.76 

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
