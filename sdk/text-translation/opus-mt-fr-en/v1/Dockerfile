FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-fr-en')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.3.3

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]