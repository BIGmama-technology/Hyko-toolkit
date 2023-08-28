FROM hyko-sdk:latest AS main

WORKDIR /app

RUN pip install openai

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]

