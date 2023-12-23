FROM hyko-sdk:latest

WORKDIR /app

RUN pip install nltk

RUN python -c "import nltk;nltk.download('punkt')"

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
