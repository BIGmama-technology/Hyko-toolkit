FROM python:3.10-slim

RUN apt update && \
    apt install -y --no-install-recommends build-essential libgl1-mesa-glx libglib2.0-0 && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install transformers[all] torch --no-cache-dir

CMD [ "bash" ]