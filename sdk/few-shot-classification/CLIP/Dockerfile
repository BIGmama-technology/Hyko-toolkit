FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "from transformers import CLIPModel, CLIPProcessor;CLIPModel.from_pretrained('openai/clip-vit-large-patch14');processor = CLIPProcessor.from_pretrained('openai/clip-vit-large-patch14')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.1.38

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]