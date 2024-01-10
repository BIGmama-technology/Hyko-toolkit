FROM torch-cuda:latest

WORKDIR /app

COPY . .

RUN poetry run python -c "from transformers import CLIPModel, CLIPProcessor;CLIPModel.from_pretrained('openai/clip-vit-large-patch14');processor = CLIPProcessor.from_pretrained('openai/clip-vit-large-patch14')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
