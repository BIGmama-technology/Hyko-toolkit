FROM hyko-sdk-gpu:latest AS build

WORKDIR /app
COPY requirements.txt .

RUN pip install -r /app/requirements.txt

RUN python -c "import torch;from transformers import AutoTokenizer;import transformers;model = 'tiiuae/falcon-7b-instruct';tokenizer = AutoTokenizer.from_pretrained(model);pipeline = transformers.pipeline('text-generation',model=model,tokenizer=tokenizer,torch_dtype=torch.bfloat16,trust_remote_code=True,device_map='auto')"

FROM build as main

COPY main.py .
COPY config.py .

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:app"]

FROM main AS metadata

CMD ["python", "-m", "config"]