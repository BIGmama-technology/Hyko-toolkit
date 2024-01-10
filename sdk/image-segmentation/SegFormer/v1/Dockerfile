FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN poetry run python -c "from transformers import AutoImageProcessor, SegformerModel;image_processor = AutoImageProcessor.from_pretrained('nvidia/mit-b0');model = SegformerModel.from_pretrained('nvidia/mit-b0')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
