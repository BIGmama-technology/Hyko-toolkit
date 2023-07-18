FROM torch-cuda:latest as main

WORKDIR /app

RUN python -c "from transformers import AutoImageProcessor, SegformerModel;image_processor = AutoImageProcessor.from_pretrained('nvidia/mit-b0');model = SegformerModel.from_pretrained('nvidia/mit-b0')"

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