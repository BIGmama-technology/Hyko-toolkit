FROM hyko-sdk:latest

WORKDIR /app

COPY . .

RUN poetry run pip install torchvision speechbrain
RUN poetry run python -c "from speechbrain.pretrained import SpectralMaskEnhancement; model = SpectralMaskEnhancement.from_hparams(source='speechbrain/metricgan-plus-voicebank')"
CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
