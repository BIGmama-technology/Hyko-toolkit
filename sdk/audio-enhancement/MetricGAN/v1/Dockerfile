FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install speechbrain
RUN pip install torchvision
RUN python -c "from speechbrain.pretrained import SpectralMaskEnhancement; model = SpectralMaskEnhancement.from_hparams(source='speechbrain/metricgan-plus-voicebank')"


RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.23

COPY . .
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]
