FROM python:3.10-slim
RUN apt update && apt install build-essential -y && rm -rf /var/lib/apt/lists/* && pip install transformers[all] torch --no-cache-dir
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update &&\
    apt-get install -y libglib2.0-0

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD [ "bash" ]