FROM torch-cuda:latest AS main

WORKDIR /app
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

RUN python -c "from transformers import OwlViTProcessor, OwlViTForObjectDetection;OwlViTProcessor.from_pretrained('google/owlvit-base-patch32');OwlViTForObjectDetection.from_pretrained('google/owlvit-base-patch32');"

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]