from .config import Inputs, Outputs, Params
import fastapi
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import cv2
import base64
import numpy as np
import torch

app = fastapi.FastAPI()
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    prompt = inputs.classes
    i_image = base64.urlsafe_b64decode(inputs.img)
    npimg = np.frombuffer(i_image, np.uint8)
    cvimg = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imwrite("Example_image.png", cvimg)
    inputs_ = processor(
        text=prompt,
        images=cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB),
        return_tensors="pt",
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs_)
    # image text similarity score:
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=-1)

    return Outputs(probs=probs.squeeze().numpy().tolist())
