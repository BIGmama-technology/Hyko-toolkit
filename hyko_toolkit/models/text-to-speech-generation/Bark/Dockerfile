FROM hyko-sdk:latest

RUN apt update && apt install -y git
RUN pip install --no-cache-dir transformers[torch]
RUN pip install --no-cache-dir accelerate
RUN pip install "git+https://github.com/suno-ai/bark.git"

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
