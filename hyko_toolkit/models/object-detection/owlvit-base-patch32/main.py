import numpy as np
import torch
from metadata import Inputs, Outputs, Params, StartupParams, func
from PIL import Image as PILImage
from PIL import ImageDraw
from transformers import OwlViTForObjectDetection, OwlViTProcessor

from hyko_sdk.io import Image


@func.on_startup
async def load(startup_params: StartupParams):
    global model
    global processor
    global device

    device = startup_params.device_map
    processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
    model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32").to(
        device
    )


@func.on_execute
async def main(inputs: Inputs, params: Params) -> Outputs:
    np_img = inputs.img.to_ndarray()
    pil_image = PILImage.fromarray(np_img)
    draw = ImageDraw.Draw(pil_image)
    texts = inputs.tags

    inputs = processor(
        text=[texts], images=torch.from_numpy(np_img).to(device), return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = (
        torch.Tensor([torch.from_numpy(np_img).size()[::-1]])
        .to(torch.int32)
        .squeeze()[1:]
        .to(device)
    )

    results = processor.post_process(
        outputs=outputs, target_sizes=torch.stack([target_sizes])
    )
    # text = inputs.tags
    boxes, scores, labels = (
        results[0]["boxes"],
        results[0]["scores"],
        results[0]["labels"],
    )
    # print(boxes,"\n", scores, "\n", labels)
    score_threshold = 0.1
    detections = []

    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        if score >= score_threshold:
            detections.append(
                {
                    "label": texts[label.item()],
                    "confidence": round(score.item(), 3),
                    "location": box,
                }
            )

    for detection in detections:
        xmin, ymin, xmax, ymax = detection["location"]
        draw.rectangle((xmin + 80, ymin, xmax + 80, ymax), outline="red", width=1)
        draw.text(
            detection["location"][:2],
            f"{detection['label']}: {detection['confidence']}",
            fill="red",
        )

    img = Image.from_ndarray(np.asarray(pil_image))

    return Outputs(output_image=img)
