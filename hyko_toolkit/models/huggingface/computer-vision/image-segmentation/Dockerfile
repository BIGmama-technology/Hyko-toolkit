FROM hyko-sdk:latest

RUN pip install --no-cache-dir transformers[torch]
RUN pip install --no-cache-dir accelerate

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
