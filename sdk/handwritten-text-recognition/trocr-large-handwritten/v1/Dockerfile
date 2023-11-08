FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install sentencepiece einops
RUN pip install transformers[all]
RUN python -c "from transformers import TrOCRProcessor, VisionEncoderDecoderModel; processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten') ; model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.15

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
