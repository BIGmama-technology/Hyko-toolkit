FROM hyko-sdk:latest

RUN apt update && apt install build-essential -y && rm -rf /var/lib/apt/lists/* && pip install transformers[all] torch --no-cache-dir


CMD [ "bash" ]