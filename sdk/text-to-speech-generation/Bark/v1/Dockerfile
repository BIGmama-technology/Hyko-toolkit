FROM torch-cuda:latest AS main

WORKDIR /app

COPY . .

RUN poetry run pip install git+https://github.com/suno-ai/bark.git
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
