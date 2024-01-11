FROM torch-cuda:latest 

WORKDIR /app

COPY . .

RUN poetry run python -c "import torch;from diffusers import StableDiffusionPipeline;repo_id = 'runwayml/stable-diffusion-v1-5';model_pipeline = StableDiffusionPipeline.from_pretrained(repo_id, torch_dtype = torch.float16);"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
