FROM torch-cuda:latest 

WORKDIR /app

COPY . .
RUN poetry run pip install sentencepiece einops
RUN poetry run python -c "import torch;from transformers import AutoTokenizer;import transformers;model = 'tiiuae/falcon-7b-instruct';tokenizer = AutoTokenizer.from_pretrained(model);pipeline = transformers.pipeline('text-generation',model=model,tokenizer=tokenizer,torch_dtype=torch.bfloat16,trust_remote_code=True,device_map='auto')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
