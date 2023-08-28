FROM hyko-sdk:latest

WORKDIR /app

RUN pip install scikit_learn

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]

