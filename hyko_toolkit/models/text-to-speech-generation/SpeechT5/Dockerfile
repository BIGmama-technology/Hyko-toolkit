FROM hyko-sdk:latest

WORKDIR /app
COPY . .

RUN poetry run pip install sentencepiece einops datasets
RUN poetry run python -c "from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan; processor = SpeechT5Processor.from_pretrained('microsoft/speecht5_tts'); model = SpeechT5ForTextToSpeech.from_pretrained('microsoft/speecht5_tts') ; vocoder = SpeechT5HifiGan.from_pretrained('microsoft/speecht5_hifigan')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
