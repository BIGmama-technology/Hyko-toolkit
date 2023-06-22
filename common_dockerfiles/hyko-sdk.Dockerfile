FROM python:3.10-slim

RUN pip install fastapi pydantic uvicorn hyko_sdk

CMD [ "bash" ]