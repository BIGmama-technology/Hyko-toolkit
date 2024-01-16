FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry run pip install nltk
RUN poetry run python -c "import nltk;nltk.download('punkt')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
