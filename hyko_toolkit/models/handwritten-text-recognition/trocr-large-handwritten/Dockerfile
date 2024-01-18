FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN poetry run pip install sentencepiece einops
RUN poetry run python -c "from transformers import TrOCRProcessor, VisionEncoderDecoderModel; processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten') ; model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
