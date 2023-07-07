FROM hyko-sdk:latest  AS main

WORKDIR /app
RUN pip install fastapi pydantic uvicorn
RUN pip install hyko_sdk==0.1.24
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]