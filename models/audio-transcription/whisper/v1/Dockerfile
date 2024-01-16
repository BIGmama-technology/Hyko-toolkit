FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN poetry run python -c "from transformers import WhisperProcessor, WhisperForConditionalGeneration; WhisperProcessor.from_pretrained('openai/whisper-large-v2');  WhisperForConditionalGeneration.from_pretrained('openai/whisper-large-v2')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
