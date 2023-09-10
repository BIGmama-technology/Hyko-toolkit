FROM hyko-sdk:latest

WORKDIR /app

RUN pip install PyPDF2

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
