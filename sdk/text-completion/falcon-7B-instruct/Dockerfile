FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install sentencepiece einops
RUN pip install transformers[all]
RUN python -c "import torch;from transformers import AutoTokenizer;import transformers;model = 'tiiuae/falcon-7b-instruct';tokenizer = AutoTokenizer.from_pretrained(model);pipeline = transformers.pipeline('text-generation',model=model,tokenizer=tokenizer,torch_dtype=torch.bfloat16,trust_remote_code=True,device_map='auto')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.1.40

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]