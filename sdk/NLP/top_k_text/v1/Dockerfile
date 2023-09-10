FROM torch-cuda:latest

WORKDIR /app
RUN pip install scikit-learn sentence_transformers

RUN python -c "from sentence_transformers import SentenceTransformer;model = SentenceTransformer('all-MiniLM-L6-v2',device='cpu')"

RUN pip install uvicorn hyko_sdk==0.4.14

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
