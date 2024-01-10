FROM torch-cuda:latest AS main

WORKDIR /app

COPY . .

RUN poetry run python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; model_name = 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli'; tokenizer = AutoTokenizer.from_pretrained(model_name) ; model = AutoModelForSequenceClassification.from_pretrained(model_name)"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
