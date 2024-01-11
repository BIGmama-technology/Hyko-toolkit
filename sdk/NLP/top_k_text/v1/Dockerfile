FROM torch-cuda:latest

WORKDIR /app

COPY . .

RUN poetry run pip install scikit-learn sentence_transformers
RUN poetry run python -c "from sentence_transformers import SentenceTransformer;model = SentenceTransformer('all-MiniLM-L6-v2',device='cpu')"
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
