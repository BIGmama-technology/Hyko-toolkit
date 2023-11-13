FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install transformers[torch]

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.16
RUN pip install timm

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
