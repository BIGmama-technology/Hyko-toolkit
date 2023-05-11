FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

