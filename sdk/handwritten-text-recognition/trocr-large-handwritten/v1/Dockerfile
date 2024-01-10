FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN pip install sentencepiece einops
RUN pip install transformers[all]
RUN python -c "from transformers import TrOCRProcessor, VisionEncoderDecoderModel; processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten') ; model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
