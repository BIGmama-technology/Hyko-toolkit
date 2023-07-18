import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import base64
import cv2
import numpy as np
app = fastapi.FastAPI()




app = fastapi.FastAPI()

model = None
feature_extractor = None
tokenizer = None

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')

@app.post(
    "/load",
    response_model=None,
)
def load():
    global model
    global feature_extractor
    global tokenizer
    if model is not None and feature_extractor is not None and tokenizer is not None:
        print("Model loaded already")
        return

    model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning").to(device) # type: ignore
    feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if model is None or feature_extractor is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    await inputs.image.wait_data()
    img = inputs.image.to_ndarray()
    pixel_values = feature_extractor(images=cv2.cvtColor(img, cv2.COLOR_BGR2RGB), return_tensors="pt").pixel_values # type: ignore
    pixel_values = pixel_values.to(device)
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    
    return Outputs(text=preds)
