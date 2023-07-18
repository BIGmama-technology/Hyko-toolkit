from config import Inputs, Outputs, Params
import fastapi
from fastapi import HTTPException
from transformers import CLIPProcessor, CLIPModel
import cv2
import torch

app = fastapi.FastAPI()
model = None
processor = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
@app.post("/load", response_model=None)
def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return

    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")



@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    prompt = inputs.classes
    img = inputs.img.decode()

    inputs_ = processor(
        text=prompt,
        images=cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        return_tensors="pt",
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs_.to(device))
    # image text similarity score:
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=-1)
    probs=probs.squeeze().numpy().tolist()
    max_index = 0
    for i in range(len(probs)):
        if probs[max_index] <= probs[i]:
            max_index = i
    
    return Outputs(output_class=inputs.classes[max_index])
