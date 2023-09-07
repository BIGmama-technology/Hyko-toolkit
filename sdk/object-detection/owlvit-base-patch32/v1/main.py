from fastapi.exceptions import HTTPException
from transformers import OwlViTProcessor, OwlViTForObjectDetection
import torch
from PIL import Image as PILImage, ImageDraw
import numpy as np
from typing import List
from pydantic import Field
from hyko_sdk import CoreModel, SDKFunction, Image


func = SDKFunction(
    description="Object detection/recogntion model, draws bounding boxes over the image if the object is in the list of tags.",
    requires_gpu=False,
)

class Inputs(CoreModel):
    img : Image = Field(..., description="Input Image")

class Params(CoreModel):
    tags : List[str] = Field(..., description="List of object(s) names to be detected")

class Outputs(CoreModel):
    output_image: Image = Field(..., description="Input image + detection bounding Boxes")


processor = None
model = None
device = torch.device("cuda:2") if torch.cuda.is_available() else torch.device('cpu')

@func.on_startup
async def load():
    global model
    global processor
    if model is not None and processor is not None:
        print("Model loaded already")
        return

    processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
    model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32").to(device) #type: ignore


@func.on_execute
async def main(inputs: Inputs, params: Params)-> Outputs:
    if model is None or processor is None:
        raise HTTPException(status_code=500, detail="Model is not loaded yet")
   
    np_img = inputs.img.to_ndarray()
    pil_image = PILImage.fromarray(np_img)
    # img.save("TEST.jpg")
    draw = ImageDraw.Draw(pil_image)
    texts = params.tags

    inputs = processor(text=[texts], images = torch.from_numpy(np_img).to(device), return_tensors='pt').to(device)

    with torch.no_grad():
        outputs = model(**inputs) #type: ignore
    
    target_sizes = torch.Tensor([torch.from_numpy(np_img).size()[::-1]]).to(torch.int32).squeeze()[1:].to(device)

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
        
    img = Image.from_ndarray(np.asarray(pil_image))
    
    return Outputs(output_image=img)
