FROM hyko-sdk:latest
RUN apt update && apt install build-essential -y && rm -rf /var/lib/apt/lists/* && pip install transformers[all] torch --no-cache-dir
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install GLib
RUN apt-get update && apt-get install -y libglib2.0-dev libnvinfer7=7.2.2-1+cuda10.2 libnvinfer-plugin7=7.2.2-1+cuda10.2

# Clean up the package cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD [ "bash" ]