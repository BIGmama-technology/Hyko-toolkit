FROM hyko-sdk-gpu:latest AS build

WORKDIR /app
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

RUN python -c "from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer;model = VisionEncoderDecoderModel.from_pretrained('nlpconnect/vit-gpt2-image-captioning');feature_extractor = ViTImageProcessor.from_pretrained('nlpconnect/vit-gpt2-image-captioning');tokenizer = AutoTokenizer.from_pretrained('nlpconnect/vit-gpt2-image-captioning')"

FROM build as main

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]