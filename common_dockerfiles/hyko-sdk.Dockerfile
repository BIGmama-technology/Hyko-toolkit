FROM python:3.10-slim

RUN pip install hyko_sdk==0.1.30 uvicorn
RUN apt update
RUN apt install ffmpeg -y
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD [ "bash" ]