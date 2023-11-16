FROM torch-cuda:latest AS main

WORKDIR /app

RUN apt update && \
    apt install ffmpeg git -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.18
RUN pip install git+https://github.com/suno-ai/bark.git

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
