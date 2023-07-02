FROM torch-cuda:latest AS main

WORKDIR /app
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

RUN python -c "from transformers import CLIPModel, CLIPProcessor;CLIPModel.from_pretrained('openai/clip-vit-large-patch14');processor = CLIPProcessor.from_pretrained('openai/clip-vit-large-patch14')"


COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]