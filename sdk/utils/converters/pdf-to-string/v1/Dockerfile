FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry add PyPDF2 pycryptodome
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
