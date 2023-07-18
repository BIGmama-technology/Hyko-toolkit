FROM hyko-sdk-gpu:latest AS build

WORKDIR /app

RUN python -c "from transformers import AutoImageProcessor, SegformerModel;image_processor = AutoImageProcessor.from_pretrained('nvidia/mit-b0');model = SegformerModel.from_pretrained('nvidia/mit-b0')"

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]