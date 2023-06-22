import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
import base64
import cv2
import numpy as np
app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if len(f"{inputs.img}") > 100:
        print(f"{inputs.img}"[:100])
    else:
        print(f"{[inputs.img]}")
    if len(inputs.img.split(",")) != 2:
        raise HTTPException(422, "Invalid base64 image. make sure there is both header and data in the base64 string")
    header, data = inputs.img.split(",")
    print(header)
    i_image = base64.urlsafe_b64decode(data)
    npimg = np.frombuffer(i_image, np.uint8)
    cvimg = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    pixel_values = feature_extractor(images=cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB), return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    
    return Outputs(text=preds)
