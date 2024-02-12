FROM hyko-sdk:latest
 

WORKDIR /app

COPY . .
RUN poetry run pip install langchain html2text 

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
