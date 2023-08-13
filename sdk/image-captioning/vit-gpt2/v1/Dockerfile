FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer;model = VisionEncoderDecoderModel.from_pretrained('nlpconnect/vit-gpt2-image-captioning');feature_extractor = ViTImageProcessor.from_pretrained('nlpconnect/vit-gpt2-image-captioning');tokenizer = AutoTokenizer.from_pretrained('nlpconnect/vit-gpt2-image-captioning')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.3.6

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]