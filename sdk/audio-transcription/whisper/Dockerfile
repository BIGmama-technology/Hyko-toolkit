FROM hyko-sdk-gpu:latest AS build

WORKDIR /app

RUN python -c "from transformers import WhisperProcessor, WhisperForConditionalGeneration; WhisperProcessor.from_pretrained('openai/whisper-large-v2');  WhisperForConditionalGeneration.from_pretrained('openai/whisper-large-v2')"

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]