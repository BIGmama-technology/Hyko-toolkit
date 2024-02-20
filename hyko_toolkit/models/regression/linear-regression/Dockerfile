FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry add --no-cache scikit_learn
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
