import fastapi
from fastapi.exceptions import HTTPException
from config import Inputs, Params, Outputs
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from hyko_sdk.io import image_to_base64
import torch
from PIL import Image, ImageDraw
import numpy as np

processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32").cuda()

app = fastapi.FastAPI()

#################################################################

# Insert the main code of the function here #################################################################


# keep the decorator, function declaration and return type the same.
# the main function should always take Inputs as the first argument and Params as the second argument.
# should always return Outputs.

@app.post("/", response_model=Outputs)
async def main(inputs: Inputs, params: Params):

    img = Image.fromarray(inputs.img.decode()[0][..., :3]).convert("RGB")
    # img.save("TEST.jpg")
    draw = ImageDraw.Draw(img)
    texts = inputs.tags

    inputs = processor(text=[texts], images = torch.from_numpy(np.array(img)).cuda(), return_tensors='pt').to("cuda")

    with torch.no_grad():
        outputs = model(**inputs)
    
    target_sizes = torch.Tensor([torch.from_numpy(np.asarray(img)).size()[::-1]]).to(torch.int32).squeeze()[1:].to("cuda")
    
    # print("Target Sizes: ", target_sizes)
    # print("Logits", outputs.logits.shape)
    # print("boxes", outputs.pred_boxes.shape)

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