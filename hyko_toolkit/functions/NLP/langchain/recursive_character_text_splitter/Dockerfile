FROM hyko-sdk:latest

RUN pip install langchain

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
