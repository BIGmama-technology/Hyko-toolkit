FROM torch-cuda:latest AS main

WORKDIR /app
RUN pip install sentencepiece einops
RUN pip install transformers[all]
RUN python -c "from transformers import BlipModel, AutoTokenizer ;  model = BlipModel.from_pretrained('Salesforce/blip-image-captioning-base'); processor = BlipProcessor.from_pretrained('Salesforce/blip-image-captioning-base')"

RUN apt update && \
    apt install ffmpeg -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn hyko_sdk==0.4.9

COPY . . 

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3000", "main:func"]

