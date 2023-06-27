from config import Inputs, Outputs, Params
import fastapi
from fastapi.exceptions import HTTPException
from transformers import CLIPProcessor, CLIPModel
import cv2
import torch

app = fastapi.FastAPI()
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    prompt = inputs.classes
    img, err = inputs.img.decode()
    if err:
        raise HTTPException(status_code = 500, detail = err.json())
    if img is None:
        raise HTTPException(status_code = 500, detail = "Unexpected Error")
    
    inputs_ = processor(
        text=prompt,
        images=cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
        return_tensors="pt",
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs_)
    # image text similarity score:
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=-1)

    return Outputs(probs=probs.squeeze().numpy().tolist())
