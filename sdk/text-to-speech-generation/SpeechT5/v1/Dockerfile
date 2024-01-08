FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install sentencepiece einops
RUN pip install transformers[all]
RUN pip install datasets
RUN python -c "from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan; processor = SpeechT5Processor.from_pretrained('microsoft/speecht5_tts'); model = SpeechT5ForTextToSpeech.from_pretrained('microsoft/speecht5_tts') ; vocoder = SpeechT5HifiGan.from_pretrained('microsoft/speecht5_hifigan')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.23

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
