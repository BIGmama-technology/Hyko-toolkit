FROM torch-cuda:latest 

WORKDIR /app

RUN pip install transformers[torch] accelerate bitsandbytes scipy

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.23

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
