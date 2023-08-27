FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "from transformers import OwlViTProcessor, OwlViTForObjectDetection;OwlViTProcessor.from_pretrained('google/owlvit-base-patch32');OwlViTForObjectDetection.from_pretrained('google/owlvit-base-patch32');"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.9

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]