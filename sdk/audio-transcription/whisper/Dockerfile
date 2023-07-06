FROM torch-cuda:latest AS build

WORKDIR /app
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

RUN python -c "from transformers import WhisperProcessor, WhisperForConditionalGeneration; WhisperProcessor.from_pretrained('openai/whisper-large-v2');  WhisperForConditionalGeneration.from_pretrained('openai/whisper-large-v2')"
RUN apt update 
RUN apt-get install ffmpeg -y

FROM build as main

COPY main.py .
COPY config.py .

RUN pip install --upgrade hyko_sdk

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]