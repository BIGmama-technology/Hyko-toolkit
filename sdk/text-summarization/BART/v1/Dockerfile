FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "from transformers import pipeline; pipeline('summarization', model='facebook/bart-large-cnn', device_map='auto')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.15

COPY . . 

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]

