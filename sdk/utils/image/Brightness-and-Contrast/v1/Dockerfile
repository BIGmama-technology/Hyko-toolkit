FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry run pip install --no-cache-dir numpy opencv-python-headless 

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
