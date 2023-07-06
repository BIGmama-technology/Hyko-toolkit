FROM python:3.10-slim

RUN pip install --upgrade hyko_sdk
RUN apt update
RUN apt install ffmpeg -y
CMD [ "bash" ]