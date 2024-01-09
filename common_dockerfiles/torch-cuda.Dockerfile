FROM hyko-sdk:latest

RUN apt update && \
    apt install -y --no-install-recommends build-essential libgl1-mesa-glx libglib2.0-0 ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN poetry add transformers[torch] diffusers[torch] accelerate sentencepiece
