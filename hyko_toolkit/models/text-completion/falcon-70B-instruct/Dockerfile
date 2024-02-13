FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN apt update && apt install -y git wget
RUN  git clone https://huggingface.co/upstage/Llama-2-70b-instruct
RUN wget https://github.com/git-lfs/git-lfs/releases/download/v3.4.0/git-lfs-linux-amd64-v3.4.0.tar.gz && \
    tar -xvf git-lfs-linux-amd64-v3.4.0.tar.gz && \
    cd git-lfs-3.4.0/ && \
    ./install.sh
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
