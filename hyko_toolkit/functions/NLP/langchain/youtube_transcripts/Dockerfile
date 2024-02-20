FROM hyko-sdk:latest

RUN pip install --no-cache-dir langchain
RUN pip install --no-cache-dir pytube
RUN pip install --no-cache-dir youtube-transcript-api

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
