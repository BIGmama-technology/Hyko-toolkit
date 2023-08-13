FROM torch-cuda:latest AS main

WORKDIR /app

RUN python -c "import torch;from diffusers import StableDiffusionPipeline;repo_id = 'runwayml/stable-diffusion-v1-5';model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16);"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.3.2

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]