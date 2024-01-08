FROM hyko-sdk:latest

WORKDIR /app

COPY . .
RUN pip install uvicorn hyko_sdk==0.4.23

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
