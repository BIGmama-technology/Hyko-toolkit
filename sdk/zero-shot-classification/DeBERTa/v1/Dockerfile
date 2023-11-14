FROM torch-cuda:latest AS main

WORKDIR /app

RUN pip install transformers[all]
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; model_name = 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli'; tokenizer = AutoTokenizer.from_pretrained(model_name) ; model = AutoModelForSequenceClassification.from_pretrained(model_name)"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.17

COPY . . 
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
