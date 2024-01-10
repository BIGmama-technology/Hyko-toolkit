FROM torch-cuda:latest AS main

WORKDIR /app

COPY . .

RUN pip install torchaudio
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
