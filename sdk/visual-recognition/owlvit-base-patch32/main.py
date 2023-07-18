import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from hyko_sdk.io import image_to_base64
import torch
from PIL import Image, ImageDraw
import numpy as np


app = fastapi.FastAPI()

processor = None
model = None
device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
@app.post("/load", response_model=None)
def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return

    processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
    model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32").to(device)


@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
    img = Image.fromarray(inputs.img.decode()[0][..., :3]).convert("RGB")
    # img.save("TEST.jpg")
    draw = ImageDraw.Draw(img)
    texts = inputs.tags

    inputs = processor(text=[texts], images = torch.from_numpy(np.array(img)).to(device), return_tensors='pt').to(device)

    with torch.no_grad():
        outputs = model(**inputs)
    
    target_sizes = torch.Tensor([torch.from_numpy(np.asarray(img)).size()[::-1]]).to(torch.int32).squeeze()[1:].to(device)

    results = processor.post_process(outputs=outputs, target_sizes=torch.stack([target_sizes]))
    # text = inputs.tags
    boxes, scores, labels = results[0]["boxes"], results[0]["scores"], results[0]["labels"]
    # print(boxes,"\n", scores, "\n", labels)
    score_threshold = 0.1
    detections = []
 
    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        if score >= score_threshold:

            detections.append({"label" : texts[label.item()],
                               "confidence" : round(score.item(), 3),
                               "location" : box})

    for detection in detections:

        xmin, ymin, xmax, ymax = detection["location"]
        draw.rectangle((xmin+80, ymin, xmax+80, ymax), outline="red", width=1)
        draw.text(detection["location"][:2], f"{detection['label']}: {detection['confidence']}", fill="red")
    return Outputs(output_image=image_to_base64(np.asarray(img)))