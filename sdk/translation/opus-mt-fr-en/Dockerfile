FROM hyko-sdk-gpu:latest AS build

WORKDIR /app

RUN python -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-fr-en')"

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]