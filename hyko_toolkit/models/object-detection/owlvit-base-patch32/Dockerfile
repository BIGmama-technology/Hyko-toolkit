FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN poetry run python -c "from transformers import OwlViTProcessor, OwlViTForObjectDetection;OwlViTProcessor.from_pretrained('google/owlvit-base-patch32');OwlViTForObjectDetection.from_pretrained('google/owlvit-base-patch32');"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
