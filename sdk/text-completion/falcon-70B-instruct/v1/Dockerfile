FROM torch-cuda:latest 

WORKDIR /app
RUN pip install transformers[torch]

RUN apt update && \
    apt install ffmpeg git wget -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/git-lfs/git-lfs/releases/download/v3.4.0/git-lfs-linux-amd64-v3.4.0.tar.gz && \
    tar -xvf git-lfs-linux-amd64-v3.4.0.tar.gz && \
    cd git-lfs-3.4.0/ && \
    ./install.sh
RUN pip install uvicorn hyko_sdk==0.4.23

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
