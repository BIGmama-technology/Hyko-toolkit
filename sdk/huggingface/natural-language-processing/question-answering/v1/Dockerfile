FROM torch-cuda:latest 

WORKDIR /app

COPY . .

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
